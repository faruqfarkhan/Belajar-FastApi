from .. import models, schemas, utils, oauth2
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, Query, APIRouter
from ..database import get_db, engine, SessionLocal
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
from  psycopg2.extras import RealDictCursor
from sqlalchemy import func
from typing import List, Dict

router = APIRouter(
     prefix="/posts",
     tags=['posts']
)





@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 1, skip:int = 0, search:  Optional[str] =""):
# def get_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = (
        db.query(models.Post, func.count(models.Votes.post_id).label("Votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  
    )

    return [{"post": post, "votes":votes} for post,votes in result]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def createpost(post: schemas.PostBase, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    db_item = models.Post(owner_id=user_id.id, **post.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
        posts = db.query(models.Post).filter(models.Post.id == id).first()

        post =  db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your {id} not found")
        
        if post[0].owner_id != get_current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform that action")
       
        return {
        "post": post[0],
        "votes": post[1]
    }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_api(id: int, response: Response, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
 
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized to perform that action")
    
    db.delete(post) 
    db.commit()   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post_data = post_query.first()

    if post_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post_data.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorized to perform that action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()