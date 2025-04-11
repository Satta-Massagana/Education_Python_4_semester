from sqlalchemy.orm import Session
from db.models.user_model import User
from db.models.group_model import Group
from db.models.user_group import user_group_association
from schemes.group import GroupCreate, GroupUpdate
from datetime import datetime
from typing import List

class GroupService:
    def __init__(self, db: Session):
        self.db = db

    def create_group(self, group_create: GroupCreate, owner_id: int) -> Group:
        """Creates a new group."""
        db_group = Group(
            name=group_create.name,
            description=group_create.description,
            owner_id=owner_id,
            created_at=datetime.utcnow()
        )
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)

        if group_create.user_ids:
            for user_id in group_create.user_ids:
                user = self.db.query(User).filter(User.id == user_id).first()
                if user:
                    db_group.users.append(user)

        self.db.commit()
        self.db.refresh(db_group)
        return db_group

    def get_group(self, group_id: int) -> Group:
        """Retrieves a group by ID."""
        return self.db.query(Group).filter(Group.id == group_id).first()

    def list_groups(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Group]: #Corrected line
        """Lists groups with pagination."""
        return self.db.query(Group).filter(Group.owner_id == owner_id).offset(skip).limit(limit).all() #Corrected line

    def update_group(self, group_id: int, group_update: GroupUpdate) -> Group:
        """Updates a group."""
        db_group = self.get_group(group_id)
        if not db_group:
            return None

        for key, value in group_update.model_dump(exclude_unset=True).items():
            if key == "user_ids":
                db_group.users.clear()
                if value:
                    for user_id in value:
                        user = self.db.query(User).filter(User.id == user_id).first()
                        if user:
                            db_group.users.append(user)
            else:
                setattr(db_group, key, value)

        self.db.commit()
        self.db.refresh(db_group)
        return db_group

    def delete_group(self, group_id: int) -> bool:
        """Deletes a group."""
        db_group = self.get_group(group_id)
        if not db_group:
            return False

        self.db.delete(db_group)
        self.db.commit()
        return True