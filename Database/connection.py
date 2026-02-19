from sqlmodel import Session, create_engine, select, SQLModel
from fastapi import Depends
from typing import Annotated
from passlib.context import CryptContext



sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args = connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)
SessionDep = Annotated[Session, Depends(get_session)]