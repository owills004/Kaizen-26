from pydantic import BaseModel, EmailStr
from typing import Optional



class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    hashed_password: str


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None