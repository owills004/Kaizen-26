from fastapi import FastAPI, Path, Depends, HTTPException, Query
from Models.users import UserRegister, UserLogin, UserUpdate, User
from Controllers.userController import create_user, get_user, get_users, delete_user, login_user, update_user
from Database.connection import SessionDep
from typing import Annotated
import uvicorn

app = FastAPI()



@app.get("/")
async def greet():
    return {"message": "Hello World"}


@app.post("/user/register")
async def register(user_in: UserRegister, db: SessionDep):
    return create_user(user_in, db)
 


@app.get("/users")
async def read_users(db: SessionDep, offset: int =0, limit: int=10):
    return get_users(db, offset, limit)
   

@app.get("/user/{user_id}")
async def read_user(user_id: int, db: SessionDep):
    return get_user(user_id, db)


@app.post("/user/login")
async def user_login(user_in: UserLogin, db: SessionDep):
    return login_user(user_in, db)



@app.put("/user/{user_id}")
async def update_user_route(user_id: int, user_in: UserUpdate, db: SessionDep):
    return update_user(user_id, user_in, db)


@app.delete("/user/{user_id}")
async def delete_user_route(user_id: int, db: SessionDep):
    return delete_user(user_id, db)


@app.put("/user/{user_id}")
async def update_user_rout(user_id: int, user_in: UserUpdate, db: SessionDep):
    return update_user(user_id, user_in, db)


if __name__ == "__main__":
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
