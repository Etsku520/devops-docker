from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
import bcrypt

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

from functools import wraps
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                if current_user.get_role().role == role:
                    unauthorized = False

                '''
                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break
                '''

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

from multiprocessing.util import register_after_fork
from application import hello

from application.messages import models
from application.messages import messages

from application.auth import models
from application.auth import views

from application.management import views

from application.groups import views
from application.groups import models


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
except:
    pass

