from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.common.config.database import Base
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    # biography = Column(String, default=True)
