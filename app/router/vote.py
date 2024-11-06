from .. import models, schemas, utils, oauth2
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, Query, APIRouter
from ..database import get_db, engine, SessionLocal
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
from  psycopg2.extras import RealDictCursor

router = APIRouter(
     prefix="/vote",
     tags=['votes']
)





@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your {vote.post_id} not found")


    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == user_id.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user_id.id} has already voted for {vote.post_id}")
        
        new_vote = models.Votes(post_id=vote.post_id, user_id=user_id.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"success": "success"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()   
        return Response(status_code=status.HTTP_204_NO_CONTENT)
