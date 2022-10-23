from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

    class Config:
        orm_model = True
