from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: int
    login: str
    firstname: Optional[str]
    surname: Optional[str]
    location: Optional[str]
    registration_time: datetime
    last_auth_time: datetime

    model_config = {
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    surname: Optional[str] = None
    location: Optional[str] = None
