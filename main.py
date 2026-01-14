import os
from flask import Flask

from view.task import task_bp
from view.auth import auth_bp
from view.user import user_bp
from db import engine
from model.models import Base

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Инициализация секретного ключа из переменной окружения или генерация случайного
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
