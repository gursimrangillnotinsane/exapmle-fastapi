from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from ..import models, schemas, utils,auth2
from sqlalchemy.orm import Session
from ..database import get_db


from fastapi.security.oauth2 import OAuth2PasswordRequestForm #is a schema which takes the first valus as username and second as password

router = APIRouter(
tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login( user_credentials:OAuth2PasswordRequestForm= Depends(), db:Session = Depends(get_db)):
 user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
 if not user:
  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
 
 if not utils.verify( user_credentials.password,user.password): #if it is true, returns token,,,,if not it raises an exception
  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
 

 access_token=auth2.create_access_token(data={"user_id": user.id})
 return{"access_token": access_token, "token_type":"bearer"}
