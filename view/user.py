from flask import Blueprint, render_template, session
from controller.user import UserController as controller

user_bp = Blueprint('user', __name__, template_folder='templates/user')


@user_bp.route("/user", methods=["GET"])
def index():
    user_id = session.get('user_id')
    user = controller.get_user_by_id(user_id)

    return render_template("user/user.html", user=user)
