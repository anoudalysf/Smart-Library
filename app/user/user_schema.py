from pydantic import BaseModel


class User_create(BaseModel):
    user_name: str
    password: str | None = None

class UserResponse(BaseModel):
    user_id: str
    username: str
    role: str

    class Config:
        orm_mode = True
