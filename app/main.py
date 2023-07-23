"""
in command promp 
    --> path operations
    --> user:postgres, password:admin
    --> *D:\python-workspace\fastapi\venv\Scripts\activate.bat --> starts venv environment
    --> uvicorn main:app --reload --> starts application code and every code changes reload the application
    --> *uvicorn app.main:app --reload  --> after main app move to app folder 
    --> pip install psycopg2 # PostgreSQL database adapter/driver for Python
    --> # for all pip install --> be sure that u are in venv.cmd terminal !! 
    --> pip install sqlalchemy # ORM
        --> pip freeze # installed packages list  
    --> pip install email-validator # user registration , email validation 
    --> pip install "passlib[bcrypt]" --> password encrypt/decrypt -- hashing
    --> pip install "python-jose[cryptography]" --> security  
             
"""

    ## ---------- CRUD -----------

# from typing import List, Optional
# from pydantic import BaseModel
# from fastapi import FastAPI, Response,status, HTTPException, Depends
# from fastapi.params import Body
# from random import randrange
# from sqlalchemy.orm import Session
# from . import models, schemas, utils # [.] dot means same folder, import all models 
# from .database import engine, get_db
# from sqlalchemy import update

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware

## need not with alembic 
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS operations started ------------

origins = ["*"] # * public API, every one can access my API 

app.add_middleware(
    CORSMiddleware, # a function that perform some sort of operations
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CORS operations ended ------------

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


## path operation
@app.get("/")
async def root():
    return {"message": "welcome to my huhu"}


"""

# title str, content str , category

# move to schema.py 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # optional 
#    rating: Optional[int]  = None


# setup connection string, connection cursor


my_posts = [{"title":"title eof post 1", "content":"content eof post 1", "id": 1} ,
    {"title":"favorite food","content":"I like pizza", "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i



"""


    
## ---------- CRUD done -----------

## ---- creating user functionality ----


## ---- creating user functionality done ---- 
