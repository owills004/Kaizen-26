from fastapi import FastAPI, Path, Depends, HTTPException, Query
from Models.users import UserRegister, UserLogin, UserUpdate, User
from sqlmodel import Session, create_engine, select, SQLModel
from typing import Annotated
from passlib.context import CryptContext
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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)
SessionDep = Annotated[Session, Depends(get_session)]






app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def greet():
    return {"message": "Hello World"}


@app.post("/user/register")
async def register(user_in: UserRegister, db: SessionDep):
    user = User(
        name = user_in.name,
        email = user_in.email,
        hashed_password = hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "message": "Registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@app.get("/users")
async def get_users(db: SessionDep, offset: int =0, limit: int=10):
    users = db.exec(select(User).offset(offset).limit(limit))
    return users.all()



@app.post("/user/login")
async def user_login(user: UserLogin, db: SessionDep):
    user = db.exec(select(User).where(User.email == user.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found, create an account")
    if not pwd_context.verify(user.hashed_password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
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

