from flask import Blueprint, render_template, request, redirect, session, flash, abort
from controller.task import TaskController as controller
import werkzeug.exceptions as exceptions

task_bp = Blueprint('task', __name__, template_folder='templates/todo')


def require_login():
    """Проверка авторизации пользователя"""
    if not session.get('logged_in'):
        flash("Please login to access this page", "error")
        return redirect('/login')
    return None


@task_bp.route("/", methods=["GET"])
def index():
    """Главная страница со списком задач"""
    if not session.get('logged_in'):
        return render_template("index.html", tasks=[])
    
    user_id = session.get('user_id')
    tasks = controller.get_all_tasks(user_id)

    return render_template("index.html", tasks=tasks)


@task_bp.route('/add_task', methods=['GET', 'POST'])
def add_task():
    """Добавление новой задачи"""
    check = require_login()
    if check:
        return check
    
    if request.method == "GET":
        return render_template("todo/add.html")

    elif request.method == "POST":
        try:
            user_id = session.get('user_id')
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()

            if not title:
                flash("Task title is required", "error")
                return render_template("todo/add.html")

            task_id = controller.add_task(user_id, title, description)
            flash("Task added successfully!", "success")
            return redirect('/')
        except ValueError as e:
            flash(str(e), "error")
            return render_template("todo/add.html")
        except Exception as e:
            flash("An error occurred while adding the task", "error")
            return render_template("todo/add.html")


@task_bp.route('/task/<task_id>', methods=['GET'])
def view_task(task_id):
    """Просмотр отдельной задачи"""
    check = require_login()
    if check:
        return check
    
    try:
        user_id = session.get('user_id')
        task = controller.get_task_by_id(int(task_id), user_id)
        
        if not task:
            flash("Task not found", "error")
            return redirect('/')
        
        return render_template("todo/task.html", task=task)
    except (ValueError, TypeError):
        flash("Invalid task ID", "error")
        return redirect('/')


@task_bp.route('/task/delete/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    """Удаление задачи"""
    check = require_login()
    if check:
        return check
    
    try:
        user_id = session.get('user_id')
        is_deleted = controller.delete_task(int(task_id), user_id)
        
        if is_deleted:
            flash("Task deleted successfully!", "success")
        else:
            flash("Task not found or you don't have permission to delete it", "error")
        
        return redirect("/")
    except (ValueError, TypeError):
        flash("Invalid task ID", "error")
        return redirect("/")


@task_bp.route('/task/done/<task_id>', methods=['GET', 'POST'])
def mark_task_done(task_id):
    """Отметить задачу как выполненную"""
    check = require_login()
    if check:
        return check
    
    try:
        user_id = session.get('user_id')
        is_done = controller.mark_as_done(int(task_id), user_id)
        
        if is_done:
            flash("Task marked as completed!", "success")
        else:
            flash("Task not found or you don't have permission to modify it", "error")
        
        return redirect("/")
    except (ValueError, TypeError):
        flash("Invalid task ID", "error")
        return redirect("/")
