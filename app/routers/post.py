from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from ..import models, schemas,auth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func 

router=APIRouter(
    prefix="/posts", 
    tags=['Posts'] # to group in fastaip/docks
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int =Depends(auth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    postses=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #contains give flexability , doesnt need to be exact the same
     #by default the join is left inner join
    results = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
    #to get post of specific user
    # postses=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()

    return results



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int =Depends(auth2.get_current_user)):
    # post_dic=post.dict()
    # post_title= post_dic['title']
    # post_content=post_dic['content']
    # post_pub=post_dic['published']
    # cursor.execute("INSERT INTO posts(title,content,punblished) VALUES (%s,%s,%s ) RETURNING * ",(post_title,post_content,post_pub)) # first %s(it means a variable) takes ther value of first post_title
    # NEW_posts = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    current_id=current_user.id
   
    new_post=models.Post(owner_id=current_id,**post.dict()) ## to take apart every element of the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
 #title st, contnet st, category,bool published etc




@router.get("/{id}", response_model=schemas.PostOut)   #{id}=variable named id string
def get_post(id:int,response: Response,db: Session = Depends(get_db),current_user:int =Depends(auth2.get_current_user)):     #to perform validation it determines whereter or not id is convertable into int
    # cursor.execute("SELECT * FROM posts WHERE id= %s", (str(id),))# id converte to srting , to convert more than single digit number into string
    # post= cursor.fetchone()
   #  post=db.query(models.Post).filter(models.Post.id==id).first()#filter to make a condition

    post= db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
       #status_code - to change the code given, detail- to give the line that will b shown
    return post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int =Depends(auth2.get_current_user)): #id is integer
    
    # cursor.execute("DELETE FROM posts WHERE ID = %s RETURNING *", (str(id),))
    # index=cursor.fetchone()
    # conn.commit()


    post= db.query(models.Post).filter(models.Post.id==id)
    post_first=post.first()
    if post.first()==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post with id doesnt exist")
    
    if post_first.owner_id!=current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NOT AUTHORIZED TO PERFORM REQUESTED METHOD")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int =Depends(auth2.get_current_user)):


    # cursor.execute("UPDATE posts set title =%s, content=%s,punblished=%s  WHERE id = %s RETURNING *", (post.title,post.content,post.published, str(id),))
    # updated_post=cursor.fetchone()
    # conn.commit()


    post_query=db.query(models.Post).filter(models.Post.id==id)
    postw=post_query.first()
    if postw==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post with id doesnt exist")  
    
    if postw.owner_id!=current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NOT AUTHORIZED TO PERFORM REQUESTED METHOD")
    post_query.update(post.dict(),synchronize_session=False) 
    db.commit()

    return post_query.first() 