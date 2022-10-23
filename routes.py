from fastapi import APIRouter
from microblog import blog
from user import api


routes = APIRouter()

routes.include_router(blog.router, prefix='/blog')
routes.include_router(api.router, prefix='/user')
