from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional



"""
class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True 

# this model updates each column
class PostUpdate(BaseModel):
    title: str
    content: str
    published: bool # = True # provide each column for update 

""
# for example this model updates only one column 
class PostUpdate(BaseModel):
    published: bool 
"""



# OR istead of define same things again and again, we can make like below

# orm_mode = True because no fields exits that we post , id, password   
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 
    
    class Config():
        orm_mode = True 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase): # extends PostBase 
    pass # which means same as PostBase

# class PostUpdate(PostBase): # no need , updating and creating fundamentally same , alsa we can create naming convention 

"""
# can be defined request model within the decorator 
# all columns or partially viewed   
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime 
    # FOR "value is not a valid dict (type=type_error.dict)" error, this tells pydantic to ignore the error and convert to dict, leave it to SQLalchemy  
    class Config():
        orm_mode = True 
"""

# no need orm_mode = True because all fields exits that we post 
class UserCreate(BaseModel):
    email: EmailStr # email validation 
    password: str
    

class Post(PostBase): # inherit PostBase, so title, content, published inherited 
    id: int
    created_at: datetime 
    owner_id: int 
    owner: UserOut
    # FOR "value is not a valid dict (type=type_error.dict)" error, this tells pydantic to ignore the error and convert to dict, leave it to SQLalchemy  
    class Config():
        orm_mode = True 

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config():
        orm_mode = True 

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = True

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)  
