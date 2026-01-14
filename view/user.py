from flask import Blueprint, render_template, session, redirect, flash
from controller.user import UserController as controller

user_bp = Blueprint('user', __name__, template_folder='templates/user')


@user_bp.route("/user", methods=["GET"])
def index():
    """Страница профиля пользователя"""
    if not session.get('logged_in'):
        flash("Please login to access this page", "error")
        return redirect('/login')
    
    user_id = session.get('user_id')
    user = controller.get_user_by_id(user_id)
    
    if not user:
        flash("User not found", "error")
        return redirect('/')
    
    return render_template("user/user.html", user=user)
