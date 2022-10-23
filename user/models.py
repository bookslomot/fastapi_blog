from sqlalchemy import Column, String, Integer, DateTime, Boolean
from core.db import Base


class UserDB(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=type, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
