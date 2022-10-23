from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.utils import get_db
from user import schemas
from user.handlers import Auth
from user.models import UserDB
from user.schemas import User

security = HTTPBearer()
auth_handler = Auth()


class CRUDUser:

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(UserDB).filter(UserDB.username == username).first()

    @staticmethod
    def get_all_users(db: Session):
        return db.query(UserDB).all()

    @staticmethod
    def sign_user(db: Session, user: dict):
        db_user = UserDB(username=user['username'], password=user['password'])
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def create_user(db: Session, user: schemas.User):
        db_user = UserDB(username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class UserEndpoints:

    @staticmethod
    def signup(user_details: schemas.User, db: Session = Depends(get_db)):
        if CRUDUser.get_user_by_username(db, user_details.username) is not None:
            return 'Account already exists'
        try:
            hashed_password = auth_handler.encode_password(user_details.password)
            user = {'username': user_details.username, 'password': hashed_password}
            return CRUDUser.sign_user(db, user)
        except:
            return 'Failed to signup user'

    @staticmethod
    def login(user_details: schemas.User, db: Session = Depends(get_db)):
        user = CRUDUser.get_user_by_username(db, user_details.username)
        if user is None:
            return HTTPException(status_code=401, detail='Invalid Username')
        if not auth_handler.verify_password(user_details.password, user.password):
            return HTTPException(status_code=401, detail='Invalid Password')
        access_token = auth_handler.encode_token(user.username)
        refresh_token = auth_handler.encode_refresh_token(user.username)
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
