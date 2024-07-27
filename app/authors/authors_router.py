from fastapi import APIRouter, Depends, HTTPException
from app.authors import authors_schema, authors_crud
from sqlalchemy.orm import Session
from app.common.config.database import get_db
from typing import Annotated, Union
from app.common.utils import auth

app = APIRouter()


# GET all authors
@app.get("/authors", tags=["author"])
def retrieve_all_authors(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    authors = authors_crud.read_all_authors(db, skip=skip, limit=limit)
    return authors


# GET a specific author
@app.get("/authors/{author_id}", response_model=authors_schema.Author, tags=["author"])
async def retrieve_specific_author(author_id: int, db: Session = Depends(get_db)):
    return authors_crud.read_author(db, author_id)


# POST a new author
@app.post("/authors/", tags=["author"])
def add_new_author(
    _: Annotated[bool, Depends(auth.RoleChecker(allowed_roles=["Admin"]))],
    author: authors_schema.Author_add,
    db: Session = Depends(get_db),
):
    return authors_crud.create_author(db, author=author)


# PUT an author by ID
@app.put("/authors/{author_id}", response_model=authors_schema.Author, tags=["author"])
async def update_author(
    _: Annotated[bool, Depends(auth.RoleChecker(allowed_roles=["Admin"]))],
    author_id: int,
    author: authors_schema.Author_add,
    db: Session = Depends(get_db),
):
    return authors_crud.update_author(db, author, author_id)


# DELETE an author by ID
@app.delete(
    "/authors/{author_id}", response_model=authors_schema.Author, tags=["author"]
)
def delete_author(
    _: Annotated[bool, Depends(auth.RoleChecker(allowed_roles=["Admin"]))],
    author_id: int,
    db: Session = Depends(get_db),
):
    db_author = authors_crud.delete_author(db, author_id=author_id)
    # if db_author is None:
    #     raise HTTPException(status_code=404, detail="Author not found")
    return db_author
