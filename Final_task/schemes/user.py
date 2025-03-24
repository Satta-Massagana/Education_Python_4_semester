from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="John")
    last_name: str = Field(..., min_length=1, max_length=50, example="Doe")
    login: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$', example="john_doe")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', example="john.doe@example.com")
    password_hash: str = Field(..., min_length=10, max_length=255, example="hashed_password")
    active: bool = Field(True, example=True)

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, example="John")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, example="Doe")
    login: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$', example="john_doe")
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', example="john.doe@example.com")
    password_hash: Optional[str] = Field(None, min_length=10, max_length=255, example="hashed_password")
    active: Optional[bool] = Field(None, example=True)
