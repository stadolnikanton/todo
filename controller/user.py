import hashlib

from flask import session as flask_session

from db import Session
from model.user import User


PASSWORD_LENGTH = 8


class UserController:

    @staticmethod
    def register(name, email, password, password_repeat):
        if len(password) < PASSWORD_LENGTH:
            raise ValueError("Password must be at least 6 characters long")

        if password != password_repeat:
            raise ValueError("Passwords do not match")

        with Session as session:
            existing_user = session.query(
                User).filter_by(email=email).first()
            if existing_user:
                raise ValueError("Username already taken")

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user = User(name=name, email=email, password=hashed_password)

            session.add(user)
            session.commit()
            session.refresh(user)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

    @staticmethod
    def login(email, password):
        if not email or not password:
            raise ValueError("Email and password are required")

        with Session as session:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = session.query(User).filter_by(
                email=email, password=hashed_password).first()

            if not user:
                raise ValueError("Invalid email or password")

            return {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }

    @staticmethod
    def get_user_by_id(user_id):
        with Session as session:
            user = session.query(User).filter_by(id=user_id).first()
            return user

    @staticmethod
    def logout():
        flask_session.clear()
