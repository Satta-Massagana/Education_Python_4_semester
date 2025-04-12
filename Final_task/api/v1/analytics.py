from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from sqlalchemy.orm import Session
from services.analytics_service import AnalyticsService
from api.v1.auth_middleware import get_current_user
from db.models.user_model import User
from db.db_conf import get_db
from schemes.analytics import PeriodExpenseResponse, GroupPeriodExpenseResponse
from db.models.user_group import user_group_association
from db.models.group_model import Group

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])

@analytics_router.get("/user/expenses/by-period", response_model=PeriodExpenseResponse)
async def get_user_expenses_by_period(
    start_date: date = Query(..., description="Start date of the period (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date of the period (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get sum of expenses for current user grouped by category within specified date range.
    """
    # проверка диапазона дат
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date must be before end date"
        )

    analytics_service = AnalyticsService(db)
    return analytics_service.get_user_expenses_by_period(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

@analytics_router.get("/group/{group_id}/expenses/by-period", response_model=GroupPeriodExpenseResponse)
async def get_group_expenses_by_period(
    group_id: int,
    start_date: date = Query(..., description="Start date of the period (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date of the period (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get sum of expenses for group members (owner + confirmed users) 
    grouped by category within specified date range.
    """
    # проверка диапазона дат
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date must be before end date"
        )

    # проверка что юзер принадлежит группе или владелец группы
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    is_member = db.query(
        user_group_association
    ).filter(
        user_group_association.c.user_id == current_user.id,
        user_group_association.c.group_id == group_id,
        user_group_association.c.confirmed == True
    ).first()

    if current_user.id != group.owner_id and not is_member:
        raise HTTPException(
            status_code=403,
            detail="You must be the owner or a confirmed member to view group analytics"
        )

    analytics_service = AnalyticsService(db)
    result = analytics_service.get_group_expenses_by_period(
        group_id=group_id,
        start_date=start_date,
        end_date=end_date
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No expenses found for this group in the specified period"
        )

    return result