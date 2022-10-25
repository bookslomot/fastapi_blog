from core.db import database
from user.models import UserDB
from .models import posts
from .schemas import PostCreate


async def get_post_list():
    return await database.fetch_all(query=posts.select())


async def creat_post(item: PostCreate):
    post = posts.insert().values(**item.dict())
    return await database.execute(post)
    # post = Post(**item.dict())
    # db.add(post)
    # db.commit()
    # db.refresh(post)
    # return post
