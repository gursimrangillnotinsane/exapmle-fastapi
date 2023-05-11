
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_password)

app=FastAPI()
origions=["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origions,#domains which 
    allow_credentials=True,
    allow_methods=["*"],# allow specific mehods(get,update)
    allow_headers=["*"],#allwo which headers
)


models.Base.metadata.create_all(bind=engine)

#import's the functions
app.include_router(post.router)#to make router work in oter files ,include router from post
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") #decorator
async def root():
    return {"message": f"Hello "}



