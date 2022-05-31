from fastapi import FastAPI

from src.domain import schemas

app = FastAPI()


@app.post("/")
async def register_user(user: schemas.UserCreate):
    return {"message": "Hello World"}
