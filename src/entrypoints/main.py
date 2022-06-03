import time

from fastapi import FastAPI, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from config import get_settings
from src.domain import schemas, models
from src.adapters.orm import get_db

settings = get_settings()

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host=settings.db_host,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as e:
        print("Connection to database failed")
        print(e)
        time.sleep(3)


@app.post("/", status_code=201, response_model=schemas.UserBase)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.password != user.password2:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    try:
        new_user = models.User(email=user.email, hashed_password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"email": new_user.email}

    except (IntegrityError, UniqueViolation):
        raise HTTPException(status_code=400, detail="User already exists")
