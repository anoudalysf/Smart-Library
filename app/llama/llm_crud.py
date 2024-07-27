import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Depends
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import VectorDBQA
from app.Books import books_model
from app.common.config.database import get_db
from langchain.schema import Document  

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Passw0rd@localhost:5432/smart_library_database"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

llm = Ollama(model="llama3.1")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

persist_directory = 'chromadb'

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

df = pd.read_csv("books_cleaned.csv")

print("Columns in the DataFrame:")
print(df.columns)

print("\nFirst few rows of the DataFrame:")
print(df.head())

columns_to_drop = ['isbn13', 'isbn10', 'subtitle']
existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
df = df.drop(columns=existing_columns_to_drop)

columns_to_check = ['title', 'categories', 'description', 'authors']
df = df.dropna(subset=columns_to_check)

columns_to_fill = ['thumbnail', 'published_year', 'average_rating', 'num_pages', 'ratings_count']
df[columns_to_fill] = df[columns_to_fill].fillna({'thumbnail': '', 'published_year': 0, 'average_rating': 0, 'num_pages': 0, 'ratings_count': 0})

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

def create_book(db: Session, book_data, embeddings, persist_directory):
    db_book = books_model.Book(
        authors=book_data['authors'],
        title=book_data['title'],
        categories=book_data['categories'],
        thumbnail=book_data.get('thumbnail', ''),
        description=book_data['description'],
        published_year=book_data.get('published_year', 0),
        average_rating=book_data.get('average_rating', 0),
        num_pages=book_data.get('num_pages', 0),
        ratings_count=book_data.get('ratings_count', 0)
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
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
            'authors': book_data['authors'],
            'title': book_data['title'],
            'categories': book_data['categories'],
            'published_year': book_data.get('published_year', 0),
            'average_rating': book_data.get('average_rating', 0),
            'num_pages': book_data.get('num_pages', 0),
            'ratings_count': book_data.get('ratings_count', 0)
        }
    )

    documents = text_splitter.split_documents([doc])
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory='chromadb')

    print(f"Persisted {len(documents)} documents to {persist_directory}")

def add_books_to_db_and_chroma(df, db, embeddings, persist_directory):
    for _, row in df.iterrows():
        book_data = row.to_dict()
        create_book(db, book_data, embeddings, persist_directory='chromadb')
        print("Book added successfully")

def main():
    db = SessionLocal()
    try:
        add_books_to_db_and_chroma(df, db, embeddings, persist_directory='chromadb')
        print("All books added successfully")
    finally:
        db.close()
    
    if os.path.exists(persist_directory):
        print(f"Persist directory '{persist_directory}' exists. Contents:")
        print(os.listdir(persist_directory))
    else:
        print(f"Persist directory '{persist_directory}' does not exist.")

if __name__ == "__main__":
    main()
