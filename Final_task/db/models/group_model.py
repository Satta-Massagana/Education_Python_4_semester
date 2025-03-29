from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from ..db_conf import Base
from .user_group import user_group_association

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship("User", secondary=user_group_association, back_populates="groups")
    owner = relationship("User", back_populates="owned_groups", foreign_keys=[owner_id])
