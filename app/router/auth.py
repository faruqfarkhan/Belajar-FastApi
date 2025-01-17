from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, responses
from sqlalchemy.orm import session
from .. import database, schemas, models, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm




router = APIRouter(
    tags=['Authentication']
)



@router.post("/login", response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: session = Depends(database.get_db),):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credential")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credential")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token":  access_token, "token_type": "bearer", "user_id": user.id} 