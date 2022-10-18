from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    id = Column(UUID, primary_key=True)
    name = Column(String, unique=True)
    date = Column(DateTime)


users = User.__table__
