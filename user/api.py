from fastapi import APIRouter, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.utils import get_db
from user import schemas
from user.services import CRUDUser, security, auth_handler
from user.schemas import User
from user.services import UserEndpoints

router = APIRouter()


@router.post('/signup')
async def signup(user_details: schemas.User):
    return await UserEndpoints.signup(user_details)


@router.post('/login')
def login(user_details: schemas.User):
    return UserEndpoints.login(user_details)


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
async def get_users():
    return await CRUDUser.get_all_users()
