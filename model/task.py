from sqlalchemy import Column, INTEGER, DateTime, ForeignKey, String
from model.user import User
from model.base import Base

from datetime import datetime


class Task(Base):
    __tablename__ = "tasks"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    owner_id = Column(INTEGER, ForeignKey(User.id))
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # status =
