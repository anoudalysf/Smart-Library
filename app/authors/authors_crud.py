from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.authors import authors_schema, authors_model


# GET all authors
def read_all_authors(db: Session, skip: int = 0, limit: int = 100):
    db_authors = db.query(authors_model.Author).offset(skip).limit(limit).all()
    if db_authors is None:
        raise HTTPException(status_code=404, detail="No authors found")
    return db_authors


# GET an author by ID
def read_author(db: Session, author_id):
    db_author = (
        db.query(authors_model.Author)
        .filter(authors_model.Author.author_id == author_id)
        .first()
    )
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


# POST a new author
def create_author(db: Session, author: authors_schema.Author_add):
    db_author = authors_model.Author(
        first_name=author.name
        # biography=author.biography,
    )
    db_other_author = (
        db.query(authors_model.Author)
        .filter(
            authors_model.Author.name == db_author.name
            # authors_model.Author.biography == db_author.biography,
        )
        .first()
    )
    if db_other_author is not None:
        raise HTTPException(status_code=409, detail="Author already added")
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author



# PUT an author by ID
def update_author(db: Session, author: authors_schema.Author_add, id):
    author_to_update = (
        db.query(authors_model.Author)
        .filter(authors_model.Author.author_id == id)
        .first()
    )
    if author_to_update is None:
        raise HTTPException(status_code=404, detail="Author not found")
    author_to_update.name = author.name
    # author_to_update.biography = author.biography
    db.commit()
    db.refresh(author_to_update)
    return author_to_update


# DELETE an author by ID
def delete_author(db: Session, author_id: int):
    db_author = (
        db.query(authors_model.Author)
        .filter(authors_model.Author.author_id == author_id)
        .first()
    )
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return db_author
