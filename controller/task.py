from db import get_session
from model.task import Task


class TaskController:
    @staticmethod
    def get_all_tasks(user_id):
        """Получить все задачи пользователя"""
        session = get_session()
        try:
            tasks = session.query(Task).filter_by(owner_id=user_id).order_by(Task.created_at.desc()).all()
            return tasks
        finally:
            session.close()

    @staticmethod
    def get_task_by_id(task_id, user_id):
        """Получить задачу по ID с проверкой владельца"""
        session = get_session()
        try:
            task = session.query(Task).filter_by(id=task_id, owner_id=user_id).first()
            return task
        finally:
            session.close()

    @staticmethod
    def add_task(user_id, title, description):
        """Добавить новую задачу"""
        if not title or not title.strip():
            raise ValueError("Task title is required")
        
        session = get_session()
        try:
            new_task = Task(owner_id=user_id, name=title.strip(),
                            description=description.strip() if description else None)

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return new_task.id
        finally:
            session.close()

    @staticmethod
    def delete_task(task_id, user_id):
        """Удалить задачу с проверкой владельца"""
        session = get_session()
        try:
            task = session.query(Task).filter_by(id=task_id, owner_id=user_id).first()

            if task:
                session.delete(task)
                session.commit()
                return True

            return False
        finally:
            session.close()

    @staticmethod
    def mark_as_done(task_id, user_id):
        """Отметить задачу как выполненную"""
        session = get_session()
        try:
            task = session.query(Task).filter_by(id=task_id, owner_id=user_id).first()

            if task:
                task.is_completed = True
                session.commit()
                return True

            return False
        finally:
            session.close()

    @staticmethod
    def update_task(task_id, user_id, title=None, description=None):
        """Обновить задачу"""
        session = get_session()
        try:
            task = session.query(Task).filter_by(id=task_id, owner_id=user_id).first()

            if not task:
                return False

            if title:
                task.name = title.strip()
            if description is not None:
                task.description = description.strip() if description else None

            session.commit()
            return True
        finally:
            session.close()
