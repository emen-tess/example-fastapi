from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] 
)

""" 
# no need, only learning purpose 
@router.get("/sqlalchemy")
def test_post(db: Session=Depends(get_db)):

    # posts = db.query(models.Post) # this only creates SQL statement but not run  
    posts = db.query(models.Post).all() # all() method RUNS SQL statement that created db.query(models.Post)
    return{"data":posts}
"""

# SQLalchemy model get
# @router.get("/posts", response_model=schemas.Post) # expect one post but we have Lists of Posts so error 
# @router.get("/", response_model=List[schemas.Post]) 
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/") # remove response model for join result , simple way 
def get_posts(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user),    
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post) # this only creates SQL statement but not run      
    ### posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # only owner_id posts
    # posts = db.query(models.Post).all() # all() method RUNS SQL statement that created db.query(models.Post)
    # posts = db.query(models.Post).limit(limit).all() # limit 
    # posts = db.query(models.Post).limit(limit).offset(skip).all() # skip  for page button 
        # {{URL}}posts?limit=3&skip=1&search=sqlalchemy%20title
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # search

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # @router.get("/") olduğu durumda gerekti 
    # posts = [{"Post": {**post.__dict__}, "votes": votes} for post, votes in posts]
    return posts

    # print(results)
    #return {"data": posts}
    # return results # posts # without "data" keyword


# SQLalchemy model post
# @router.post("/posts",status_code=status.HTTP_201_CREATED) # without request model
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # with request model 
def create_posts(post:schemas.PostCreate, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # what if posts table have 50 colums ? 
    # new_user = models.Post(**post.dict()) # matches ALL columns with post parameter
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return{"data":new_post}
    return new_post

 # SQLalchemy model post
@router.get("/{id}",response_model=schemas.PostOut ) # path parameter
def get_post(id:int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    print(id) 
    ## row = db.query(models.Post).filter(models.Post.id==id).first() ## join öncesi
    row = db.query(models.Post, func.count(
        models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(
            models.Post.id==id).first()
    
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"row with id : {id} was not found")

    # if row.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                     detail=f"Not authorized to perform requested action")


    # return{"post_detail": row} 
    return row




 # SQLalchemy model delete
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#    delete_row= db.query(models.Post)
#    if delete_row.first() == None:
    delete_row = db.query(models.Post).filter(models.Post.id==id).first()
    if not delete_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"row with id : {id} was not found")
    
    if delete_row.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    db.delete(delete_row)
    db.commit()
    print(delete_row)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# SQLalchemy model update 
# put ile update yapılacaksa tüm alanlar gönderilmeli !
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # request comes in schema (class)

    updated_query = db.query(models.Post).filter(models.Post.id==id)

    updated_row = updated_query.first()

    if not updated_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"row with id : {id} was not found")
    
    if updated_row.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    updated_query.update(post.dict())
    db.commit()
    print(updated_row)
    # return{"post_detail": updated_query.first()}  
    return updated_query.first()

""" 
# SCHEMA/PYDANTIC model get 
@router.get("/posts")
def get_posts():
    # return {"data":"this is the posts"}
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    print("Total rows are:  ", len(posts))
    print("Printing each row")

    print(posts)
    # return {"data":my_posts}
    return {"data": posts}

@router.post("/createposts")
def create_posts(payload: dict = Body(...)) :
    print(payload)
    return{"message":"succesfully created posts"}
#   return{"new_user":f"title {payload['title']} content {payload['content']}"}

# @router.post("/posts") # status code verilmezse 200 OK dönüyor 
@router.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()

    # print(post) # assumes dictionary
    # print(post.rating)
    # print(post.dict())
    # return{"data":"post"}
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return{"data":post_dict}

# SCHEMA/PYDANTIC model post
# @router.post("/posts") # status code verilmezse 200 OK dönüyor 
@router.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    # cursor.execute(f"INSERT INTO products (title, content, published) VALUES ({post.title}, {post.content}, {post.published})") # if user enters "INSERT INTO xxx" for title that corrupts data !!!
    # put quotation marks surround SQL statement !!
    cursor.execute(INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * , (post.title, post.content, post.published)) # SQL injection, with %s placeholders psycopg2 (SQL library) sanitizes the input , make sures parameters safe
    new_user = cursor.fetchone()
    conn.commit()
    return{"data":new_user}
 """

# eğer bu metod aşağıdaki @router.get("/posts/{id}") altında olsaydı hata alırdı
# çünkü ilk karşılaştığı metod o olacağı için /posts/{id} --> id = "latest" parametre olarak kabul edecekti.
# # bu nedenle sıralama önemli , parametre alanlar sonda olmalı 
# yada başka bir anahtar kelime olmalı  @router.get("/posts/RECENT/latest") 
# @router.get("/latest") 
# def get_latest_post():
#     post = my_posts[len(my_posts)-1] 
#     return{"detail":post}

"""
@router.get("/posts/{id}") # path parameter
# def get_post(id:int, response:Response): ## httperror ile gerek kalmayacak 
def get_post(id:int): 
    print(id)
    post = find_post(int(id))
    if not post:
        # response.status_code = 404 #status code manipulation 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"message": f"post with id : {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not foundd")
    # post = find_post(int(id))
    print(post)
    # return{"post_detail": f"Here is post {id}"} 
    return{"post_detail": post}  


# SCHEMA/PYDANTIC model get
@router.get("/posts/{id}") # path parameter
def get_post(id:int): 
    print(id)    
    # put quotation marks surround SQL statement !!
    # cursor.execute(SELECT * FROM posts WHERE id = %s,(id,))
    # cursor.execute(SELECT * FROM posts WHERE id = %s,[id])
    cursor.execute(SELECT * FROM posts WHERE id = %s ,(str(id),))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"row with id : {id} was not found")
    print(row)
    return{"post_detail": row}  


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    my_posts.pop(index)
    # return {"message":"post successfully deleted"} # silince herhangi bir şey geri dönmez  
    return Response(status_code=status.HTTP_204_NO_CONTENT) # delete için zorunlu return value 


# SCHEMA/PYDANTIC model delete 
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # put quotation marks below 
    cursor.execute(DELETE FROM posts WHERE id = %s RETURNING *,(str(id),))
    delete_row = cursor.fetchone()
    # if delete_row == None:
    if not delete_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"row with id : {id} was not found")
    conn.commit()                                                        
    print(delete_row)
    return{"post_detail": delete_row}  


# put ile update yapılacaksa tüm alanlar gönderilmeli !
@router.put("/posts/{id}")
def update_post(id:int, post:Post): # request comes in schema (class)

    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")

    post_dict = post.dict()
    post_dict["id"]=id
    my_posts[index]=post_dict  

    print(post)
    return {"data":post_dict}
    # return {"message":"post updated"}

# SCHEMA/PYDANTIC model update 
# put ile update yapılacaksa tüm alanlar gönderilmeli !
@router.put("/posts/{id}")
def update_post(id:int, post:Post): # request comes in schema (class)
    # put quotation marks below
    cursor.execute(UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * ,(post.title, post.content,str(id)))
    update_row = cursor.fetchone()
    if not update_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"row with id : {id} was not found")
    conn.commit()                                                        
    print(update_row)
    return{"post_detail": update_row}  

"""

