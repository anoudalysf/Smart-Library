from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.common.config.database import get_db
from app.Books import books_crud, books_schema
from typing import Annotated
from app.common.utils import auth
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings


app = APIRouter()


embeddings = OllamaEmbeddings(model="nomic-embed-text")
persist_directory = 'chromadb'

# GET /books: Retrieve a list of all books.
@app.get("/books/", response_model=list[books_schema.Books], tags=["books"])
def retrieve_all_books(start: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return books_crud.get_books(db, start=start, limit=limit)


# POST /books: Create a new book record (Admin only).
@app.post("/books/", tags=["books"])
async def create_book(
    _: Annotated[bool, Depends(auth.RoleChecker(allowed_roles=["Admin"]))],
    book: books_schema.Books_create,
    db: Session = Depends(get_db)
):
    try:
        print(f"Received book in router: {book}")
        print(f"Type of book: {type(book)}")
        return books_crud.create_book(db, book)
    except Exception as e:
        print(f"An error occurred in router: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# GET /books/:id: Retrieve details of a specific book by its ID.
@app.get("/books/{id}", response_model=books_schema.Books, tags=["books"])
async def retrieve_single_book(id: int, db: Session = Depends(get_db)):
    return books_crud.get_single_book(db, id)


# PUT /books/:id: Update an existing book record by its ID (Admin only).
@app.put("/books/{id}", response_model=books_schema.Books_create, tags=["books"])
async def update_book(
    _: Annotated[bool, Depends(auth.RoleChecker(allowed_roles=["Admin"]))],
    id: int,
    book: books_schema.Books_create,
    db: Session = Depends(get_db),
):
    return books_crud.update_book(db, book, id)


# DELETE /books/:id: Delete a book record by its ID (Admin only).
@app.delete("/books/{id}", response_model=books_schema.Books_create, tags=["books"])
async def delete_book(
    _: Annotated[bool, Depends(auth.RoleChecker(allowed_roles=["Admin"]))],
    id: int,
    db: Session = Depends(get_db),
):
    return books_crud.delete_book(db, id)


# GET /recommendations: Retrieve book recommendations for the user based on their preferences.
@app.get(
    "/recommendations/{user_id}",
    response_model=list[books_schema.Books],
    tags=["recommendations"],
)
async def recommend_book(user_id: str, db: Session = Depends(get_db)):
    try:
        recommendations = books_crud.recommend_book(db, user_id)
        return recommendations
    except Exception as e:
        print(f"An error occurred while getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# GET /recommendations: Retrieve book recommendations for the user based on their query
@app.get("/recommendation_query", response_model=list[books_schema.Books], tags=["recommendations"])
async def recommend_books_from_query(user_query: str, db: Session = Depends(get_db)):
    try:
        recommendations = books_crud.recommend_books_from_query(db, user_query)
        return recommendations
    except Exception as e:
        print(f"An error occurred while getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))