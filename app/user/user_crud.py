from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid
from app.common.utils import auth
from app.user.user_model import User
from app.user.user_schema import User_create
from app.Books import books_schema, books_model


def get_user_byId(db: Session, user_id: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user


def get_user_by_username(db: Session, user_name: str):
    user = db.query(User).filter(User.username == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user


def check_register(db: Session, user_name: str):
    if db.query(User).filter(User.username == user_name).first():
        raise HTTPException(status_code=400, detail="Username is already registered")


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user: User_create, user_id: str):
    db_user = get_user_byId(db, user_id)

    hashed_password = auth.get_password_hash(user.password)
    db_user.username = user.user_name
    db_user.password_hash = hashed_password

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "user_id": db_user.user_id,
        "username": db_user.username,
        "role": db_user.role,
    }


def create_user(db: Session, user: User_create):
    check_register(db, user.user_name)
    uid = uuid.uuid4()
    stringified_uid = str(uid)
    hashed_password = auth.get_password_hash(user.password)

    db_user = User(
        user_id=stringified_uid,
        username=user.user_name,
        password_hash=hashed_password,
        role="User",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user_id": stringified_uid, "username": user.user_name, "role": "User"}


def delete_user(db: Session, user_id: str):
    user_to_delete = (
        db.query(User).filter(User.user_id == user_id).first()
    )
    if user_to_delete.role == "Admin":
        raise HTTPException(status_code=400, detail="Cannot delete an admin user.")
    db.delete(user_to_delete)
    db.commit()
    return {"user_id": user_to_delete.user_id, "username": user_to_delete.user_name, "role": user_to_delete.role} 


def add_preference(
    db: Session, preference: books_schema.User_preferences_create, user_id: str
):
    db_preference = books_model.User_preference(
        user_id=user_id,
        preferences=preference.preferences,
    )
    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference
