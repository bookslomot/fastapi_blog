from starlette.requests import Request

from core.db import SessionLocal


def get_db():
    return SessionLocal()
