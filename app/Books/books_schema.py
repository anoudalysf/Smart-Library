from pydantic import BaseModel
from typing import Optional

class Books(BaseModel):
    book_id: int
    authors: str
    title: str
    categories: str
    thumbnail: Optional[str] = None
    description: str
    published_year: Optional[int] = None
    average_rating: Optional[float] = None
    num_pages: Optional[int] = None
    ratings_count: Optional[int] = None

    class Config:
        orm_mode = True

class Books_create(BaseModel):
    authors: str
    title: str
    categories: str
    thumbnail: Optional[str] = None
    description: str
    published_year: Optional[int] = None
    average_rating: Optional[float] = None
    num_pages: Optional[int] = None
    ratings_count: Optional[int] = None

    class Config:
        orm_mode = True



class User_preferences(BaseModel):
    preference_id: int
    user_id: str
    book_id: int


class User_preferences_create(BaseModel):
    user_id: str
    book_id: int