from pydantic import BaseModel


class Logs(BaseModel):
    Logs_ID: int
    User_ID: str
    TimeStamp: str
    Endpoint: str
    Method_Type: str


class Add_logs(BaseModel):
    Logs_ID: int
    User_ID: str
    TimeStamp: str
    Endpoint: str
    Method_Type: str
