from flask import Blueprint, render_template, request, redirect, session
from controller.task import TaskController as controller
import werkzeug.exceptions as exceptions

task_bp = Blueprint('task', __name__, template_folder='templates/todo')


@task_bp.route("/", methods=["GET"])
def index():
    user = session.get('user_id')
    tasks = controller.get_all_tasks(user)

    return render_template("index.html", tasks=tasks)


@task_bp.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == "GET":
        return render_template("todo/add.html")

    elif request.method == "POST":
        user = session.get('user_id')
        title = request.form["title"]
        description = request.form["description"]

        controller.add_task(user, title, description)

        return redirect('/')


@task_bp.route('/task/delete/<task_id>', methods=['GET'])
def delete_task(task_id):
    try:
        is_deleted = controller.delete_task(task_id)
    except ValueError:
        return None

    if is_deleted:
        return redirect("/")

    raise exceptions.BadRequest("Post not found")
