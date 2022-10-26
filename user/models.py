from sqlalchemy import Column, String, Integer

from core.db import Base


class UserDB(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=type, unique=True)
    username = Column('username', String, unique=True)
    password = Column(String)


users = UserDB.__table__
