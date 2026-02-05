from fastapi import FastAPI
from Models.users import UserRegister, UserLogin, UserUpdate
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


@app.put("/user/update")
async def update_user(user: UserUpdate):
    name = user.name
    password = user.password
    return {
        "message": "Updated successfully",
        "user": user
    }