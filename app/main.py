from app.database import engine
from . import models
from app.config import settings
from fastapi import FastAPI
from app.router import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind=engine)




app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def login():
    return {"tes":"tes"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




    