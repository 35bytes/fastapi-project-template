from fastapi import FastAPI, HTTPException, Depends
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.domain import schemas, models
from src.adapters.orm import get_db

app = FastAPI()


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
