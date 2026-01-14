import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Создание движка базы данных
DB_URL = os.environ.get("DB_URL", "sqlite:///todo.db")
engine = create_engine(DB_URL, echo=False)

# Создание фабрики сессий
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    """Получить новую сессию базы данных"""
    return SessionLocal()
