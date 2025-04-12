from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from db.models.transaction_model import Transaction
from db.models.user_group import user_group_association
from db.models.group_model import Group

from schemes.analytics import PeriodExpenseResponse, CategoryExpense, GroupPeriodExpenseResponse

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_expenses_by_period(
        self, 
        user_id: int, 
        start_date: date, 
        end_date: date
    ) -> PeriodExpenseResponse:
        results = self.db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total_amount')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'Expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(
            Transaction.category
        ).all()


        total_expenses = sum(result.total_amount for result in results)

        categories = [
            CategoryExpense(
                category=result.category,
                total_amount=result.total_amount
            ) for result in results
        ]

        return PeriodExpenseResponse(
            start_date=start_date,
            end_date=end_date,
            categories=categories,
            total_expenses=total_expenses
        )

    def get_group_expenses_by_period(
        self,
        group_id: int,
        start_date: date,
        end_date: date
    ) -> GroupPeriodExpenseResponse:

        group = self.db.query(Group).filter(Group.id == group_id).first()
        if not group:
            return None

        confirmed_members = self.db.query(
            user_group_association.c.user_id
        ).filter(
            user_group_association.c.group_id == group_id,
            user_group_association.c.confirmed == True
        ).all()

        member_ids = [member.user_id for member in confirmed_members] + [group.owner_id]

        results = self.db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total_amount')
        ).filter(
            Transaction.user_id.in_(member_ids),
            Transaction.type == 'Expense',
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(
            Transaction.category
        ).all()

        total_expenses = sum(result.total_amount for result in results)

        categories = [
            CategoryExpense(
                category=result.category,
                total_amount=result.total_amount
            ) for result in results
        ]

        return GroupPeriodExpenseResponse(
            group_id=group_id,
            start_date=start_date,
            end_date=end_date,
            categories=categories,
            total_expenses=total_expenses
        )
