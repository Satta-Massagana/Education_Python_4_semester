from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date

class CategoryExpense(BaseModel):
    category: str
    total_amount: float

class PeriodExpenseResponse(BaseModel):
    start_date: date
    end_date: date
    categories: List[CategoryExpense]
    total_expenses: float
    model_config = ConfigDict(from_attributes=True)

class GroupPeriodExpenseResponse(BaseModel):
    group_id: int
    start_date: date
    end_date: date
    categories: List[CategoryExpense]
    total_expenses: float
    model_config = ConfigDict(from_attributes=True)