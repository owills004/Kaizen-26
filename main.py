from fastapi import FastAPI, Path
from Models.users import UserRegister, UserLogin, UserUpdate
from typing import Annotated
import uvicorn


app = FastAPI()


@app.get("/")
async def greet():
    return {"message": "Hello World"}


@app.post("/user/register")
async def register(user: UserRegister):
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

