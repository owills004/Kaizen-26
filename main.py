from fastapi import FastAPI, Path, Depends
from Models.users import UserRegister, UserLogin, UserUpdate
from typing import Annotated
import uvicorn
import json


app = FastAPI()

def get_db():
    with open("database.json", "r") as f:
        return json.load(f)

def save_db(db):
    with open('database.json', 'w') as f:
        json.dump(db, f, indent=2)



@app.get("/")
async def greet():
    return {"message": "Hello World"}


@app.post("/user/register")
async def register(user: UserRegister, db: dict = Depends(get_db)):
    db['users'].append(user)
    save_db(db)
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

