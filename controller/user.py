import hashlib

from flask import session as flask_session

from db import get_session
from model.user import User


PASSWORD_LENGTH = 8


class UserController:

    @staticmethod
    def register(name, email, password, password_repeat):
        """Регистрация нового пользователя"""
        if not name or not name.strip():
            raise ValueError("Name is required")
        
        if not email or not email.strip():
            raise ValueError("Email is required")
        
        if len(password) < PASSWORD_LENGTH:
            raise ValueError(f"Password must be at least {PASSWORD_LENGTH} characters long")

        if password != password_repeat:
            raise ValueError("Passwords do not match")

        session = get_session()
        try:
            existing_user = session.query(User).filter_by(email=email.strip()).first()
            if existing_user:
                raise ValueError("Email already taken")

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user = User(name=name.strip(), email=email.strip(), password=hashed_password)

            session.add(user)
            session.commit()
            session.refresh(user)

            return {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        finally:
            session.close()

    @staticmethod
    def login(email, password):
        """Вход пользователя"""
        if not email or not password:
            raise ValueError("Email and password are required")

        session = get_session()
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = session.query(User).filter_by(
                email=email.strip(), password=hashed_password).first()

            if not user:
                raise ValueError("Invalid email or password")

            return {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        finally:
            session.close()

    @staticmethod
    def get_user_by_id(user_id):
        """Получить пользователя по ID"""
        if not user_id:
            return None
        
        session = get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            return user
        finally:
            session.close()

    @staticmethod
    def logout():
        """Выход пользователя"""
        flask_session.clear()
