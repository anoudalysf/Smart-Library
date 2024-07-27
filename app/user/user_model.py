from sqlalchemy import Column, String
from app.common.config.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="User")
