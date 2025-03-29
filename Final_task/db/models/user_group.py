from sqlalchemy import Column, Integer, ForeignKey, Table, Boolean
from ..db_conf import Base

user_group_association = Table(
    'user_group_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('confirmed', Boolean, default=False)
)
