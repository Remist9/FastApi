from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: int
    login: str

    model_config = {
        "from_attributes": True
    }
