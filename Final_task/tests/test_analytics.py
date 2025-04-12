import pytest
from fastapi import status
from datetime import date, timedelta, datetime
from sqlalchemy.orm import Session
from db.models.user_model import User
from db.models.group_model import Group
from db.models.transaction_model import Transaction
from db.models.user_group import user_group_association

TEST_USER_ID = 1
TEST_GROUP_ID = 1
TEST_CATEGORY = "Food"
TEST_AMOUNT = 100.50

global_id = 1

@pytest.fixture
def test_data(db_session: Session, auth_headers):
    """Create test data with unique group IDs"""
    global global_id

    test_user_id = auth_headers["user_id"]

    group_id = int(datetime.now().timestamp()) % 10000000
    group_id += global_id
    global_id += 1
    group = Group(
        id=group_id,
        name=f"Test Group {group_id}",
        description="Test Description",
        owner_id=test_user_id,
        created_at=date.today()
    )
    db_session.add(group)
    db_session.commit()

    today = date.today()
    transactions = [
        Transaction(
            category=TEST_CATEGORY,
            amount=TEST_AMOUNT,
            currency="USD",
            description="Test transaction",
            type="Expense",
            date=today - timedelta(days=1),
            user_id=test_user_id
        ),
        Transaction(
            category="Transport",
            amount=50.25,
            currency="USD",
            description="Another transaction",
            type="Expense",
            date=today,
            user_id=test_user_id
        )
    ]
    db_session.add_all(transactions)

    stmt = user_group_association.insert().values(
        user_id=test_user_id,
        group_id=group_id,
        confirmed=True
    )
    db_session.execute(stmt)
    db_session.commit()
    
    return {"user_id": test_user_id, "group_id": group_id}


def test_get_user_expenses_by_period(test_app, test_data, auth_headers):
    """Test /user/expenses/by-period endpoint"""
    today = date.today()
    start_date = (today - timedelta(days=7)).isoformat()
    end_date = today.isoformat()
    
    response = test_app.get(
        f"/analytics/user/expenses/by-period",
        params={"start_date": start_date, "end_date": end_date},
        headers=auth_headers["header"]
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["start_date"] == start_date
    assert data["end_date"] == end_date
    assert len(data["categories"]) > 0
    assert any(cat["category"] == TEST_CATEGORY for cat in data["categories"])
    assert data["total_expenses"] == pytest.approx(100.5)


def test_get_group_expenses_by_period(test_app, test_data, auth_headers):
    """Test /group/{group_id}/expenses/by-period endpoint"""
    today = date.today()
    start_date = (today - timedelta(days=7)).isoformat()
    end_date = today.isoformat()
    
    response = test_app.get(
        f"/analytics/group/{test_data['group_id']}/expenses/by-period",
        params={"start_date": start_date, "end_date": end_date},
        headers=auth_headers["header"]
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["group_id"] == test_data['group_id']
    assert data["start_date"] == start_date
    assert data["end_date"] == end_date
    assert len(data["categories"]) > 0
    assert data["total_expenses"] == pytest.approx(100.5)

def test_get_group_expenses_unauthorized(test_app, test_data):
    """Test group analytics with unauthorized access"""
    today = date.today()
    response = test_app.get(
        f"/analytics/group/{test_data['group_id']}/expenses/by-period",
        params={
            "start_date": (today - timedelta(days=7)).isoformat(),
            "end_date": today.isoformat()
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_invalid_date_range(test_app, auth_headers):
    """Test with invalid date range (start_date > end_date)"""
    today = date.today()
    response = test_app.get(
        "/analytics/user/expenses/by-period",
        params={
            "start_date": today.isoformat(),
            "end_date": (today - timedelta(days=1)).isoformat()
        },
        headers=auth_headers["header"]
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Start date must be before end date" in response.json()["detail"]
