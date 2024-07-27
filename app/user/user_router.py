from fastapi import APIRouter, Depends, HTTPException

from app.user.user_schema import User_create
from app.user import user_crud, user_model
from app.common.config.database import get_db
from typing import Annotated
from app.common.utils import auth
from sqlalchemy.orm import Session
from app.Books import books_schema


app = APIRouter()


@app.post("/users/register", tags=["users"])
def create_user(user: User_create, db: user_crud.Session = Depends(get_db)):
    return user_crud.create_user(db, user)


@app.post("/users/login", tags=["users"])
async def login_for_access_token(
    form_data: Annotated[auth.OAuth2PasswordRequestForm, Depends()],
    db: user_crud.Session = Depends(get_db),
) -> auth.Token:
    return auth.access_token(db, form_data.username, form_data.password)


@app.get("/users/me/", tags=["users"])
async def read_users_me(
    current_user: Annotated[user_model.User, Depends(auth.get_current_user)],
):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "role": current_user.role,
    }


@app.put("/users/me/{user_id}", tags=["users"])
async def update_users_me(
    user_id: str, user: User_create, db: user_crud.Session = Depends(get_db)
):
    return user_crud.update_user(db, user, user_id)


@app.post("/users/me/preference/{user_id}", tags=["users"])
async def add_user_preference(
    user_id: str,
    preference: books_schema.User_preferences_create,
    db: Session = Depends(get_db),
):
    return user_crud.add_preference(db, preference, user_id)
