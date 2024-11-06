from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import time
from app.config import settings
from  psycopg2.extras import RealDictCursor
from sqlalchemy.orm import sessionmaker


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres" ,password="C0mpn3t!", cursor_factory=RealDictCursor )
#         cur = conn.cursor()
#         print("connection succes")
#         break
#     except Exception as error:
#         print("error, ", error)
#         print("connection to database failed")
#         time.sleep(2)


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()