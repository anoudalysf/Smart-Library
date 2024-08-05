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


# GET /books/:title: Retrieve details of a specific book by its title.
@app.get("/books/{title}", response_model=books_schema.Books, tags=["books"])
async def retrieve_book_by_title(title: str, db: Session = Depends(get_db)):
    return books_crud.get_book_by_title(db, title)


# GET /books/:id: Retrieve details of a specific book by its ID.
@app.get("/books/{id}", response_model=books_schema.Books, tags=["books"])
async def retrieve_book_by_id(id: int, db: Session = Depends(get_db)):
    return books_crud.get_book_by_id(db, id)



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
    
# GET /chat_with_bot: Retrieve chat response from the bot based on user query
@app.get("/chat_with_bot", response_model=str, tags=["chat"])
async def chat_with_bot_endpoint(user_query: str, db: Session = Depends(get_db)):
    try:
        chat_response = books_crud.chat_with_bot(db, user_query)
        return chat_response
    except Exception as e:
        print(f"An error occurred while chatting with the bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# GET /books/sorted/rating_desc: Retrieve a list of books sorted by rating in descending order.
@app.get("/books/sorted/rating_desc", response_model=list[books_schema.Books], tags=["books"])
def retrieve_books_sorted_by_rating_desc(start: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return books_crud.get_books_sorted_by_rating_desc(db, start=start, limit=limit)

# GET /books/sorted/rating_asc: Retrieve a list of books sorted by rating in ascending order.
@app.get("/books/sorted/rating_asc", response_model=list[books_schema.Books], tags=["books"])
def retrieve_books_sorted_by_rating_asc(start: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return books_crud.get_books_sorted_by_rating_asc(db, start=start, limit=limit)

    
# GET /books/sorted/year_desc: Retrieve a list of books sorted by published year in descending order.
@app.get("/books/sorted/year_desc", response_model=list[books_schema.Books], tags=["books"])
def retrieve_books_sorted_by_rating_desc(start: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return books_crud.get_books_sorted_by_year_desc(db, start=start, limit=limit)

# GET /books/sorted/year_asc: Retrieve a list of books sorted by published year in ascending order.
@app.get("/books/sorted/year_asc", response_model=list[books_schema.Books], tags=["books"])
def retrieve_books_sorted_by_rating_asc(start: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return books_crud.get_books_sorted_by_year_asc(db, start=start, limit=limit)

# Add a new user preference
@app.post("/user_preferences/", tags=["user_preferences"])
async def add_user_preference(
    preference: books_schema.User_preferences_create,
    db: Session = Depends(get_db)
):
    return books_crud.add_user_preference(db, preference)

# Get user preferences (liked books)
@app.get("/user_preferences/{user_id}", response_model=list[books_schema.Books], tags=["user_preferences"])
async def get_user_preferences(user_id: str, db: Session = Depends(get_db)):
    return books_crud.get_user_preferences(db, user_id)

# Delete a user preference
@app.delete("/user_preferences/", tags=["user_preferences"])
async def delete_user_preference(
    preference: books_schema.User_preferences_create,
    db: Session = Depends(get_db)
):
    return books_crud.delete_user_preference(db, preference)
