from fastapi import FastAPI, Path, Depends, HTTPException, Query
from Models.users import UserRegister, UserLogin, UserUpdate
from sqlmodel import Session, create_engine, select, SQLModel
from typing import Annotated
import uvicorn



sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args = connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]






app = FastAPI()




@app.get("/")
async def greet():
    return {"message": "Hello World"}


@app.post("/user/register")
async def register(user: UserRegister, db: SessionDep):
    db.add(user)
    db.commit()
    return {
        "message": "Registered successfully",
    }

@app.post("/user/login")
async def user_login(user: UserLogin):
    return {
        "message": "Logged in successfully"
    }


@app.put("/user/{user_id}")
async def update_user(user_id: Annotated[int, Path(title="User ID")], user: UserUpdate, q:str | None = None):
    results = {'user': user_id}
    if q: 
        results.update({'q': q})
    if user:
        results.update({'user': user})
    return results

