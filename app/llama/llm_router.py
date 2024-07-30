from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.common.config.database import get_db
from app.Books import books_crud  
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

app = APIRouter()

@app.post("/add-books")
def add_books_to_db_and_chroma(file_path: str, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file_path)
        
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        chroma_db = Chroma(persist_directory="/Users/aalyousef001/My_Smart_Library/Smart-Library/app/llama/chromadb", embedding_function=embeddings)
        
        for _, row in df.iterrows():
            book_data = row.to_dict()
            books_crud.create_book(db, book_data, embeddings, persist_directory='/Users/aalyousef001/My_Smart_Library/Smart-Library/app/llama/chromadb')
        
        return {"message": "Books added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

