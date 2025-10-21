from datetime import datetime

from sqlalchemy import Column, INTEGER, String, DateTime
from model.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    register_date = Column(DateTime, default=datetime.utcnow)
