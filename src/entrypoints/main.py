from fastapi import FastAPI, HTTPException

from src.domain import schemas

app = FastAPI()


@app.post("/", status_code=201)
async def register_user(user: schemas.UserCreate):
    if user.password != user.password2:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    return None
