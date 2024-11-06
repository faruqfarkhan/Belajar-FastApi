from .. import models, schemas, utils
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, Query, APIRouter
from ..database import get_db, engine, SessionLocal
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
import time


router = APIRouter(
    prefix="/users",
    tags=['users']
)



@router.get("/", response_model=list[schemas.UserOut])
def get_user(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createpost(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"your {id} not found")        

    return user
