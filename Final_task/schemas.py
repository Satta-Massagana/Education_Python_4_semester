from pydantic import BaseModel, Field
from typing import Optional, Literal

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

class TransactionCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=50, example="string")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3, pattern=r'^[A-Z]{3}$', example="RUB")
    description: str = Field(..., min_length=1, max_length=255, example="string")
    type: Literal['Expense', 'Income'] = Field(..., example="Expense")
    user_id: int = Field(..., gt=0)

class TransactionUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=50, example="string")
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3, pattern=r'^[A-Z]{3}$', example="RUB")
    description: Optional[str] = Field(None, min_length=1, max_length=255, example="string")
    type: Optional[Literal['Expense', 'Income']] = Field(None, example="Expense")
    user_id: Optional[int] = Field(None, gt=0)
