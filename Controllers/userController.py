from Models.users import UserRegister, UserLogin, UserUpdate, User
from sqlmodel import select
from Database.connection import SessionDep, pwd_context, hash_password


def create_user(user_in: UserRegister, db: SessionDep):
    user = User(name=user_in.name, email=user_in.email, 
                hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        'message': "User created successfully",
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    }



def login_user(user_in: UserLogin, db:SessionDep):
    user = db.exec(select(User).where(User.email == user_in.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found, create an account")
    
    if not pwd_context.verify(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {
        'ok': True,
        'message': "Logged in successfully",
    }



def get_user(user_id: int, db: SessionDep) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user



def get_users(db: SessionDep, offset: int=0, limit:int=10) -> list[User]:
    users = db.exec(select(User).offset(offset).limit(limit)).all()
    return users



def update_user(user_id: int, user_in: UserUpdate, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user_in.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        if key == "password":
            setattr(user, "hashed_password", hash_password(value))
        else:
            setattr(user, key, value)
            
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        'message': "User updated successfully",
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    }


def delete_user(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {
        'message': "User deleted successfully",
        'ok': True
    }

def update_user(user_id: int, user: UserUpdate, db: SessionDep):
    user_db = db.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return {
        'message': "User updated successfully",
        'user': user_db
    }