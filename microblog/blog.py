from typing import List
from fastapi import APIRouter, Depends

from core.utils import get_db
from user.models import UserDB
from . import service
from .schemas import PostCreate, PostList

router = APIRouter()


@router.get('/', response_model=List[PostList])
async def post_lst():
    return await service.get_post_list()


@router.post('/')
async def post_create(item: PostCreate):
    return await service.creat_post(item)
