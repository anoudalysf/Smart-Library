from sqlalchemy import Column, Integer, String, Float
from app.common.config.database import Base


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    authors = Column(String, index=True)
    title = Column(String, index=True)
    categories = Column(String, index=True)
    thumbnail = Column(String, index=True)
    description = Column(String, index=True)
    published_year = Column(Integer, index=True)
    average_rating = Column(Float, index=True)
    num_pages = Column(Integer, index=True)
    ratings_count = Column(Integer, index=True)
    # author_id = Column(Integer, index=True)
    


class User_preference(Base):
    __tablename__ = "userpreferences"

    preference_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    book_id = Column(Integer, primary_key=True,index=True)
