from sqlalchemy import Column, String
from app.common.config.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="User")

    preferences = relationship("User_preference", back_populates="user", cascade="all, delete-orphan")