from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, json_schema_extra={"example": "John"})
    last_name: str = Field(..., min_length=1, max_length=50, json_schema_extra={"example": "Doe"})
    login: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$', json_schema_extra={"example": "john_doe"})
    email: str = Field(..., pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', json_schema_extra={"example": "john.doe@example.com"})
    password: str = Field(..., min_length=10, max_length=255, json_schema_extra={"example": "password"})
    active: bool = Field(True, json_schema_extra={"example": True})

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, json_schema_extra={"example": "John"})
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, json_schema_extra={"example": "Doe"})
    login: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$', json_schema_extra={"example": "john_doe"})
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', json_schema_extra={"example": "john.doe@example.com"})
    password_hash: Optional[str] = Field(None, min_length=10, max_length=255, json_schema_extra={"example": "password"})
    active: Optional[bool] = Field(None, json_schema_extra={"example": True})

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    login: str

    model_config = ConfigDict(from_attributes=True)
