from sqlalchemy.orm import Session
from app.Books import books_model, books_schema
from sqlalchemy.orm import Session
from app.authors import authors_model
from app.Books import books_services
import pandas as pd
from app.authors import authors_schema, authors_crud
from langchain.schema import Document 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re


embeddings = OllamaEmbeddings(model="nomic-embed-text")
persist_directory = '/Users/aalyousef001/Proj_FastAPI/Smart-Library/app/llama/chromadb'

def get_books(db: Session, start: int = 0, limit: int = 100):
    start = abs(start)
    limit = min(max(limit, 1), 100)
    list_of_books = db.query(books_model.Book).offset(start).limit(limit).all()
    books_services.check_books(repr(list_of_books))
    return list_of_books


def create_book(db: Session, book_data: books_schema.Books_create):
    try:
        #for debugging (not printing for some reason)
        print(f"Received book_data: {book_data}")
        print(f"Type of book_data: {type(book_data)}")
        print(f"Book data authors: {book_data.authors}")

        db_book = books_model.Book(
            authors=book_data.authors,
            title=book_data.title,
            categories=book_data.categories,
            thumbnail=book_data.thumbnail,
            description=book_data.description,
            published_year=book_data.published_year,
            average_rating=book_data.average_rating,
            num_pages=book_data.num_pages,
            ratings_count=book_data.ratings_count
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        content = (
            f"Authors: {book_data.authors}\n"
            f"Title: {book_data.title}\n"
            f"Categories: {book_data.categories}\n"
            f"Published Year: {book_data.published_year or 0}\n"
            f"Average Rating: {book_data.average_rating or 0}\n"
            f"Number of Pages: {book_data.num_pages or 0}\n"
            f"Ratings Count: {book_data.ratings_count or 0}\n"
            f"Description: {book_data.description}"
        )
        doc = Document(
            page_content=content,
            metadata={
                'authors': book_data.authors,
                'title': book_data.title,
                'categories': book_data.categories,
                'published_year': book_data.published_year or 0,
                'average_rating': book_data.average_rating or 0.0,
                'num_pages': book_data.num_pages or 0,
                'ratings_count': book_data.ratings_count or 0
            }
        )

        documents = text_splitter.split_documents([doc])
        vector_store = Chroma.from_documents(documents, embeddings, persist_directory='/Users/aalyousef001/Proj_FastAPI/Smart-Library/app/llama/chromadb')
        vector_store.persist()

        return db_book
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    
def update_book(db: Session, book: books_schema.Books_create, id: int):
    book_to_update = (
        db.query(books_model.Book).filter(books_model.Book.book_id == id).first()
    )
    books_services.check_single_book(book_to_update)
    book_to_update.title = book.title
    book_to_update.categories = book.categories
    book_to_update.description = book.description
    book_to_update.authors = book.authors
    book_to_update.published_year = book.published_year
    book_to_update.average_rating = book.average_rating
    book_to_update.thumbnail = book.thumbnail
    book_to_update.num_pages = book.num_pages
    book_to_update.ratings_count = book.ratings_count
    db.commit()
    db.refresh(book_to_update)
    return book_to_update


def get_book_by_id(db: Session, id):
    book_to_get = (
        db.query(books_model.Book).filter(books_model.Book.book_id == id).first()
    )
    books_services.check_single_book(book_to_get)
    return book_to_get

def get_book_by_title(db: Session, title: str):
    book_to_get = (
        db.query(books_model.Book).filter(books_model.Book.title == title).first()
    )
    # books_services.check_single_book(book_to_get)
    return book_to_get



def delete_book(db: Session, id):
    book_to_delete = (
        db.query(books_model.Book).filter(books_model.Book.book_id == id).first()
    )
    books_services.check_single_book(book_to_delete)
    db.delete(book_to_delete)
    db.commit()
    return book_to_delete

# a function to normalize the titles from the llm to make it easier to fetch from the database 
# (realized theres no need but leaving for future improving)
def normalize_title(title):
    """Normalize book title by removing special characters and converting to lowercase."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', title).strip().lower()


def recommend_book(db: Session, user_id: str):
    preference = (
        db.query(books_model.User_preference)
        .filter(books_model.User_preference.user_id == user_id)
        .first()
    )
    books_services.check_preference(preference)

    books = (
        db.query(books_model.Book)
        .filter(books_model.Book.categories.contains(preference.preferences))
        .all()
    )
    books_services.check_books(repr(books))

    books_list = "\n".join([f"{book.title} by {book.authors}" for book in books])
    context = f"Based on the user's preference for {preference.preferences}, recommend the best books from the following list:\n{books_list}\n\nRecommendation:"

    llm = Ollama(model="llama3.1")

    custom_prompt = PromptTemplate(template="{context}\n\n{query}", input_variables=["context", "query"])

    llm_chain = LLMChain(prompt=custom_prompt, llm=llm)

    #debugging
    print(f"Context: {context}")
    print(f"LLM: {llm}")
    print(f"Prompt Template: {custom_prompt}")

    try:
        input_dict = {"context": context, "query": "Recommend books"}
        print(f"Input Dict: {input_dict}")
        result = llm_chain(input_dict) 
        recommendations_text = result["text"]
        print(f"Recommendations: {recommendations_text}")
        
        recommended_books = []
        for book in books:
            if book.title in recommendations_text:
                recommended_books.append({
                    "book_id": book.book_id,
                    "authors": book.authors,
                    "title": book.title,
                    "categories": book.categories,
                    "thumbnail": book.thumbnail,
                    "description": book.description,
                    "published_year": book.published_year,
                    "average_rating": book.average_rating,
                    "num_pages": book.num_pages,
                    "ratings_count": book.ratings_count
                })

        if not recommended_books:
            raise ValueError("No books found in the recommendation response.")

        return recommended_books
    except Exception as e:
        print(f"An error occurred during recommendation: {e}")
        raise e


def recommend_books_from_query(db: Session, user_query: str):
    books = db.query(books_model.Book).all()
    books_services.check_books(repr(books))

    books_list = "\n".join([f"{book.title} by {book.authors}" for book in books])
    context = f"Based on the user's query, '{user_query}', recommend the best books from the following list:\n{books_list}\n\nRecommendation:"

    llm = Ollama(model="llama3.1")

    custom_prompt = PromptTemplate(template="{context}\n\n{query}", input_variables=["context", "query"])

    llm_chain = LLMChain(prompt=custom_prompt, llm=llm)

    #debugging
    print(f"Context: {context}")
    print(f"LLM: {llm}")
    print(f"Prompt Template: {custom_prompt}")

    try:
        input_dict = {"context": context, "query": user_query}
        print(f"Input Dict: {input_dict}")
        result = llm_chain(input_dict) 
        recommendations_text = result["text"]
        print(f"Recommendations: {recommendations_text}")
        
        title_pattern = re.compile(r"\*\*(.*?)\*\*")
        recommended_titles = title_pattern.findall(recommendations_text)
        print(f"Extracted Titles: {recommended_titles}")

        normalized_titles = [normalize_title(title) for title in recommended_titles]
        print(f"Normalized Titles: {normalized_titles}")

        #to match with my database
        recommended_books = []
        for title in normalized_titles:
            for book in books:
                if normalize_title(book.title) == title:
                    recommended_books.append({
                        "book_id": book.book_id,
                        "authors": book.authors,
                        "title": book.title,
                        "categories": book.categories,
                        "thumbnail": book.thumbnail,
                        "description": book.description,
                        "published_year": book.published_year,
                        "average_rating": book.average_rating,
                        "num_pages": book.num_pages,
                        "ratings_count": book.ratings_count
                    })

        if not recommended_books:
            raise ValueError("No books found in the recommendation response.")

        return recommended_books
    except Exception as e:
        print(f"An error occurred during recommendation: {e}")
        raise e


template="""
    As a highly knowledgeable librarian good at searching documents, your role is to accurately answer book questions 
    with only the use of the data given to you from the collection of book titles and descriptions using our specialized book database.
    Make the user feel comfortable and lightly converse when needed.
    You do not need to be stringent with the keywords in the question related to these topics.
    Otherwise, tell the user you don't have what they're looking for.
    Do not suggest any books outside of our database 
    Provide the results in plain text without any additional formatting or special characters.
    Do NOT whatsoever add ANY special characters such as '\n' or quotes '"'
    Example of correct response:
    Title: Book Title.
    Description: The book description.
    DO NOT FORMAT YOUR TEXT, ONLY USE COMMAS AND DOTS WHEN NEEDED!!!!!!!!



    Book Query:
    {context}

    Query: 
    {query}"""

custom_prompt = PromptTemplate(template=template, input_variables=["context", "query"])


def chat_with_bot(db: Session, user_query: str):
    context = f"User query: '{user_query}'"

    llm = Ollama(model="llama3.1")

    llm_chain = LLMChain(prompt=custom_prompt, llm=llm)

    try:
        input_dict = {"context": context, "query": user_query}
        result = llm_chain(input_dict)
        chat_response = result["text"]

        # clean up the response
        chat_response = chat_response.strip()

        return chat_response
    except Exception as e:
        print(f"An error occurred during chat with bot: {e}")
        raise e
    
def get_books_sorted_by_rating_desc(db: Session, start: int = 0, limit: int = 100):
    start = abs(start)
    limit = min(max(limit, 1), 100)
    list_of_books = db.query(books_model.Book).order_by(books_model.Book.average_rating.desc()).offset(start).limit(limit).all()
    books_services.check_books(repr(list_of_books))
    return list_of_books

def get_books_sorted_by_rating_asc(db: Session, start: int = 0, limit: int = 100):
    start = abs(start)
    limit = min(max(limit, 1), 100)
    list_of_books = db.query(books_model.Book).order_by(books_model.Book.average_rating.asc()).offset(start).limit(limit).all()
    books_services.check_books(repr(list_of_books))
    return list_of_books

def get_books_sorted_by_year_desc(db: Session, start: int = 0, limit: int = 100):
    start = abs(start)
    limit = min(max(limit, 1), 100)
    list_of_books = db.query(books_model.Book).order_by(books_model.Book.published_year.desc()).offset(start).limit(limit).all()
    books_services.check_books(repr(list_of_books))
    return list_of_books

def get_books_sorted_by_year_asc(db: Session, start: int = 0, limit: int = 100):
    start = abs(start)
    limit = min(max(limit, 1), 100)
    list_of_books = db.query(books_model.Book).order_by(books_model.Book.published_year.asc()).offset(start).limit(limit).all()
    books_services.check_books(repr(list_of_books))
    return list_of_books

def add_user_preference(db: Session, preference_data: books_schema.User_preferences_create):
    db_preference = books_model.User_preference(
        user_id=preference_data.user_id,
        book_id=preference_data.book_id
    )
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference

def get_user_preferences(db: Session, user_id: str):
    preferences = db.query(books_model.User_preference).filter(books_model.User_preference.user_id == user_id).all()
    book_ids = [preference.book_id for preference in preferences]
    books = db.query(books_model.Book).filter(books_model.Book.book_id.in_(book_ids)).all()
    return books

def delete_user_preference(db: Session, preference_data: books_schema.User_preferences_create):
    preference = db.query(books_model.User_preference).filter_by(
        user_id=preference_data.user_id,
        book_id=preference_data.book_id
    ).first()
    if preference:
        db.delete(preference)
        db.commit()
    return preference
