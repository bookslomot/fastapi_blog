from typing import Union, Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta


class Auth:

    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    ALGORITHM = 'H256'
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'  # should be ENV
    JWT_REFRESH_SECRET_KEY = 'JWT_REFRESH_SECRET_KEY'  # should be ENV

    hasher = CryptContext(schemes=['bcrypt'])

    def encode_password(self, password: str):
        return self.hasher.hash(password)

    def verify_password(self, password, encode_password):
        return self.hasher.verify(password, encode_password)

    @classmethod
    def create_token(cls, subject: Union[str, Any],
                     token_minutes: int,
                     jwt_secret: str,
                     expires_delta: timedelta = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=token_minutes)

        encode = {'exp': expires_delta, 'sub': str(subject)}
        encode_jwt = jwt.encode(encode, jwt_secret, cls.ALGORITHM)
        return encode_jwt

    @classmethod
    def create_access_token(cls, subject: Union[str, Any], expires_delta: timedelta = None) -> str:
        return cls.create_token(
            subject,
            cls.ACCESS_TOKEN_EXPIRE_MINUTES,
            cls.JWT_SECRET_KEY,
            expires_delta
        )

    @classmethod
    def create_refresh_token(cls, subject: Union[str, Any], expires_delta: timedelta = None) -> str:
        return cls.create_token(
            subject,
            cls.REFRESH_TOKEN_EXPIRE_MINUTES,
            cls.JWT_REFRESH_SECRET_KEY,
            expires_delta
        )
