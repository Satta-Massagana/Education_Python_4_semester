from pydantic import BaseModel, Field
from typing import Optional, Literal

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
