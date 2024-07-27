from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.common.config.database import Base
from sqlalchemy.orm import relationship


class Logs(Base):
    __tablename__ = "logs"

    Logs_ID = Column(Integer, primary_key=True)
    User_ID = Column(String, unique=True, index=True)
    TimeStamp = Column(String, unique=True, index=True)
    Endpoint = Column(String, unique=True, index=True)
    Method_Type = Column(String, default=True)
