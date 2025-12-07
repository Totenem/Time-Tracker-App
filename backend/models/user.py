from pydantic import BaseModel
from datetime import datetime

class UserAuth(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
