from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db_conf import get_db
from services.group_service import GroupService
from schemes.group import GroupCreate, GroupUpdate, GroupList
from db.models.user_model import User
from typing import List

groups_router = APIRouter(prefix="/groups", tags=["groups"])

@groups_router.post("/", response_model=GroupUpdate, status_code=status.HTTP_201_CREATED)
def create_group(group_create: GroupCreate, owner_id: int, db: Session = Depends(get_db)):
    """Creates a new group."""
    # Ensure the owner exists (optional, but recommended)
    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner not found")

    group_service = GroupService(db)
    return group_service.create_group(group_create, owner_id)

@groups_router.get("/{group_id}", response_model=GroupList)
def get_group(group_id: int, db: Session = Depends(get_db)):
    """Retrieves a group by ID."""
    group_service = GroupService(db)
    db_group = group_service.get_group(group_id)
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return db_group

@groups_router.get("/", response_model=List[GroupList])
def list_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lists groups with pagination."""
    group_service = GroupService(db)
    return group_service.list_groups(skip, limit)

@groups_router.put("/{group_id}", response_model=GroupUpdate)
def update_group(group_id: int, group_update: GroupUpdate, db: Session = Depends(get_db)):
    """Updates a group."""
    group_service = GroupService(db)
    db_group = group_service.update_group(group_id, group_update)
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return db_group

@groups_router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """Deletes a group."""
    group_service = GroupService(db)
    if not group_service.delete_group(group_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return None
