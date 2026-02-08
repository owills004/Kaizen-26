from pydantic import BaseModel, EmailStr, model_validator
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)
    hashed_password: str 


class UserRegister(BaseModel):
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)
    confirm_password: str = Field(nullable=False)

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegister':
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self


class UserLogin(BaseModel):
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)