from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password2: str


class UserOutput(BaseModel):
    email: EmailStr
