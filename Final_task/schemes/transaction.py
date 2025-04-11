from pydantic import BaseModel, Field
from typing import Optional, Literal

class TransactionCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=50, json_schema_extra={"example": "Food"})
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3, pattern=r'^[A-Z]{3}$', json_schema_extra={"example": "RUB"})
    description: str = Field(..., min_length=1, max_length=255, json_schema_extra={"example": "Lunch"})
    type: Literal['Expense', 'Income'] = Field(..., json_schema_extra={"example": "Expense"})
    user_id: int = Field(..., gt=0)

class TransactionUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=50, json_schema_extra={"example": "Food"})
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3, pattern=r'^[A-Z]{3}$', json_schema_extra={"example": "RUB"})
    description: Optional[str] = Field(None, min_length=1, max_length=255, json_schema_extra={"example": "Lunch"})
    type: Optional[Literal['Expense', 'Income']] = Field(None, json_schema_extra={"example": "Expense"})
    user_id: Optional[int] = Field(None, gt=0)
