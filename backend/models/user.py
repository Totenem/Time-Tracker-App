from pydantic import BaseModel, Field
from datetime import datetime

class UserSignup(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(format="email")
    password: str = Field(min_length=8, max_length=20)

class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=20)

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
