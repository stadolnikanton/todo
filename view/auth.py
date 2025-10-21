from flask import Blueprint, flash, render_template, request, redirect, session
from controller.user import UserController as controller

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth/')


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    elif request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            password_repeat = request.form["password_repeat"]

            user_data = controller.register(
                name, email, password, password_repeat)

            session['user_id'] = user_data['id']
            session['user_name'] = user_data['name']
            session['user_email'] = user_data['email']
            session['logged_in'] = True

            flash(f"Registration succesful! Welcome, {
                  user_data['name']}", "success")

            return redirect("/")

        except ValueError as e:
            flash(str(e), "error")
            return render_template("auth/register.html")
        except Exception as e:
            flash("An error occurred during registration", "error")
            return render_template("auth/register.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    elif request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]

            user_data = controller.login(email, password)

            # Сохраняем пользователя в сессии
            session['user_id'] = user_data['id']
            session['user_name'] = user_data['name']
            session['user_email'] = user_data['email']
            session['logged_in'] = True

            flash(f"Welcome back, {user_data['name']}!", "success")
            return redirect("/")

        except ValueError as e:
            flash(str(e), "error")
            return render_template("auth/login.html")
        except Exception as e:
            flash("An error occurred during login", "error")
            return render_template("auth/login.html")


@auth_bp.route('/logout')
def logout():
    controller.logout()
    flash("You have been logged out successfully", "success")
    return redirect("/")
