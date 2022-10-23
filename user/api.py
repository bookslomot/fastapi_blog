from fastapi import APIRouter, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.utils import get_db
from user import schemas
from user.handlers import Auth
from user.services import CRUDUser
from user.schemas import User
from user.services import UserEndpoints

router = APIRouter()

security = HTTPBearer()
auth_handler = Auth()


@router.post('/signup')
def signup(user_details: schemas.User, db: Session = Depends(get_db)):
    return UserEndpoints.signup(user_details, db)


@router.post('/login')
def login(user_details: schemas.User, db: Session = Depends(get_db)):
    return UserEndpoints.login(user_details, db)


@router.get('/refresh_token')
def refresh_token(credential: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credential.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}


@router.post('/add-user/', response_model=User)
def create_user(user: User,
                db: Session = Depends(get_db),
                credential: HTTPAuthorizationCredentials = Security(security)):

    return UserEndpoints.create_user(user, db, credential)


@router.get('/get-user/')
def get_user(username: str, db: Session = Depends(get_db)):
    return UserEndpoints.get_user(username, db)


@router.get('/get-users')
def get_users(db: Session = Depends(get_db)):
    return CRUDUser.get_all_users(db)
