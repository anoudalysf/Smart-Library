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

def get_books(db: Session, start: int = 0, limit: int = 6500):
    start = abs(start)
    limit = min(max(limit, 1), 6500)
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
            f"Authors: {book_data['authors']}\n"
            f"Title: {book_data['title']}\n"
            f"Categories: {book_data['categories']}\n"
            f"Published Year: {book_data.get('published_year', 0)}\n"
            f"Average Rating: {book_data.get('average_rating', 0)}\n"
            f"Number of Pages: {book_data.get('num_pages', 0)}\n"
            f"Ratings Count: {book_data.get('ratings_count', 0)}\n"
            f"Description: {book_data['description']}"
        )
        doc = Document(
            page_content=content,
            metadata={
                'authors': book_data.authors,
                'title': book_data.title,
                'categories': book_data.categories,
                'published_year': book_data.published_year,
                'average_rating': book_data.average_rating,
                'num_pages': book_data.num_pages,
                'ratings_count': book_data.ratings_count
            }
        )

        documents = text_splitter.split_documents([doc])
        vector_store = Chroma.from_documents(documents, embeddings, persist_directory='/Users/aalyousef001/Proj_FastAPI/Smart-Library/app/llama/chromadb')
        vector_store.persist()

        return db_book
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


def get_single_book(db: Session, id):
    book_to_get = (
        db.query(books_model.Book).filter(books_model.Book.book_id == id).first()
    )
    books_services.check_single_book(book_to_get)
    return book_to_get


def update_book(db: Session, book: books_schema.Books_create, id):
    book_to_update = (
        db.query(books_model.Book).filter(books_model.Book.book_id == id).first()
    )
    books_services.check_single_book(book_to_update)
    author = (
        db.query(authors_model.Author)
        .filter(authors_model.Author.author_id == book.author_id)
        .first()
    )
    books_services.check_author(author)
    book_to_update.title = book.title
    book_to_update.categories = book.categories
    book_to_update.description = book.description
    book_to_update.authors = book.authors
    db.commit()
    db.refresh(book_to_update)
    return book_to_update


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
