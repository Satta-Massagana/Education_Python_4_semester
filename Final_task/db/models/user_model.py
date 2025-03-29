from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..db_conf import Base
from .user_group import user_group_association

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)

    transactions = relationship("Transaction", back_populates="user")
    groups = relationship("Group", secondary=user_group_association, back_populates="users")
    owned_groups = relationship("Group", back_populates="owner", foreign_keys='Group.owner_id')
