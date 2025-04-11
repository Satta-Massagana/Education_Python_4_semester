from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db_conf import get_db
from services.group_service import GroupService
from schemes.group import GroupCreate, GroupUpdate, GroupList
from db.models.user_model import User
from typing import List
from api.v1.auth_middleware import get_current_user, User

groups_router = APIRouter(prefix="/groups", tags=["groups"])

@groups_router.post("/", response_model=GroupList, status_code=status.HTTP_201_CREATED)
def create_group(group_create: GroupCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Creates a new group."""
    group_service = GroupService(db)
    return group_service.create_group(group_create, user.id)

@groups_router.get("/{group_id}", response_model=GroupList)
def get_group(group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Retrieves a group by ID."""
    group_service = GroupService(db)
    db_group = group_service.get_group(group_id)
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if db_group.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this group")
    return db_group

@groups_router.get("/", response_model=List[GroupList])
def list_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Lists groups with pagination."""
    group_service = GroupService(db)
    return group_service.list_groups(user.id, skip, limit)

@groups_router.put("/{group_id}", response_model=GroupList)
def update_group(group_id: int, group_update: GroupUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Updates a group."""
    group_service = GroupService(db)
    db_group = group_service.get_group(group_id)
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if db_group.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this group")

    db_group = group_service.update_group(group_id, group_update)
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return db_group

@groups_router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Deletes a group."""
    group_service = GroupService(db)

    db_group = group_service.get_group(group_id)
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if db_group.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this group")

    if not group_service.delete_group(group_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return None
