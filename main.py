import os
from flask import Flask

from view.task import task_bp
from view.auth import auth_bp
from view.user import user_bp

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.secret_key = RANDOM_KEY

app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
