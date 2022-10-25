from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List


class PostBase(BaseModel):
    title: str
    text: str

    class Config:
        orm_mode = True


class PostList(PostBase):
    id: int
    date: datetime


class PostSingle(PostList):
    children: List[PostBase]


class PostCreate(PostBase):
    parent_id: Optional[int] = None




