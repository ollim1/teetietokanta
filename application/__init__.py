from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import os

# using postgresql on heroku
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tea.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# login
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään käyttääksesi tätä toimintoa."

# roles in login_required
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user or not current_user.is_authenticated:
                print("user not authenticated")
                return login_manager.unauthorized()
            unauthorized = False
            if role != "ANY":
                unauthorized = True
                user_role = current_user.role_object
                if user_role and user_role.name == role:
                    unauthorized = False
                elif user_role:
                    print("role: " + role + ", user role: " + user_role.name)
            if unauthorized:
                print("user unauthorized")
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# application
from application.tea import models
from application.auth import models

from application.auth.models import User, Role
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# creating user roles automatically
@event.listens_for(Role.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Role(name="admin"))
    db.session.add(Role(name="user"))
    db.session.commit()

try:
    db.create_all()
except:
    pass

# raw sql statements require the database to be formatted
from application import views
from application.tea import views
from application.auth import views
