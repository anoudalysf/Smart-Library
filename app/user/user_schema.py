from pydantic import BaseModel


class User_create(BaseModel):
    user_name: str
    password: str | None = None
