from db import Session
from model.task import Task


class TaskController:
    @staticmethod
    def get_all_tasks(user):
        with Session as session:
            tasks = session.query(Task).filter_by(owner_id=user).all()
            return tasks

    @staticmethod
    def add_task(user_id, title, description):
        with Session as session:
            new_task = Task(owner_id=user_id, name=title,
                            description=description)

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return new_task.id

    @staticmethod
    def delete_task(task_id):
        with Session as session:
            task = session.query(Task).filter(Task.id == task_id).first()

            if task:
                session.delete(task)
                session.commit()

                return True

        return False
