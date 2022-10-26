from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.db import database
from core.utils import get_db
from user import schemas
from user.handlers import Auth
from user.models import UserDB, users
from user.schemas import User

security = HTTPBearer()
auth_handler = Auth()


class CRUDUser:

    @staticmethod
    async def get_user_by_username(username: str):
        return await database.fetch_one(query=users.select().where(users.c.username == username))

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(query=users.select())

    @staticmethod
    async def sign_user(user: schemas.User):
        sign_user = users.insert().values(**user.dict())
        return await database.execute(sign_user)

    @staticmethod
    def create_user(db: Session, user: schemas.User):
        db_user = UserDB(username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class UserEndpoints:

    @staticmethod
    async def signup(user_details: schemas.User):
        user = await CRUDUser.get_user_by_username(user_details.username)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exist'
            )
        try:
            hashed_password = auth_handler.encode_password(user_details.password)
            user_details.password = hashed_password
            return await CRUDUser.sign_user(user_details)
        except:
            return 'Failed to signup user'

    @staticmethod
    async def login(user_details: schemas.User):
        user = await CRUDUser.get_user_by_username(user_details.username)
        if user is None:
            return HTTPException(status_code=401, detail='Invalid Username')
        if not auth_handler.verify_password(user_details.password, user.password):
            return HTTPException(status_code=401, detail='Invalid Password')
        access_token = auth_handler.create_access_token(user.username)
        refresh_token = auth_handler.create_refresh_token(user.username)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    @staticmethod
    def create_user(user: User,
                    db: Session = Depends(get_db),
                    credential: HTTPAuthorizationCredentials = Security(security)):
        token = credential.credentials
        if auth_handler.decode_token(token):
            return CRUDUser.create_user(db=db, user=user)
        return 'Invalid token'

    @staticmethod
    def get_user(username: str, db: Session = Depends(get_db)):
        db_user = CRUDUser.get_user_by_username(db, username=username)
        if db_user is None:
            raise HTTPException(status_code=404, detail='User not found')
        return db_user
