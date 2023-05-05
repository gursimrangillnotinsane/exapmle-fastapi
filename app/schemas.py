from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
#to put condition on input  
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):#inherits all the fields of postbase
    pass
    
class UserResponce(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True

        
#to put an condition on responce ,,, only these fields will be shown
class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner: UserResponce
    
    class Config:
        orm_mode=True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str




class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)


    