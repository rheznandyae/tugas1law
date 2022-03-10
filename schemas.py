from datetime import datetime
from os import access
from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    password: str
    full_name: str
    npm: str
    client_id:str
    client_secret:str


    class Config:
        orm_mode = True

class Token(BaseModel):
    id:int
    token:str
    timestamp:datetime
    owner_id:str

    class Config:
        orm_mode = True

class RequestToken(BaseModel):
    username: str
    password: str
    grant_type : str
    client_id : str
    client_secret  : str


