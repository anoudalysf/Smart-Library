from datetime import datetime
from fastapi import Request, Depends
from functools import wraps
from sqlalchemy.orm import Session
from app.common.config.database import get_db
from app.Logs import logs_model, logs_schema


def log_request_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request") or args[0]
        db: Session = kwargs.get("db")
        log_request(request, db)
        return await func(*args, **kwargs)

    return wrapper


def log_request(request: Request, db: Session):
    timestamp = datetime.now().isoformat()
    endpoint = request.url.path
    method = request.method
    user_id = request.headers.get("user-id", "Unknown")
    print(timestamp, endpoint, user_id, method)

    log_entry = logs_model.Logs(
        User_ID=user_id, TimeStamp=timestamp, Endpoint=endpoint, Method_Type=method
    )
    db.add(log_entry)
    db.commit()
