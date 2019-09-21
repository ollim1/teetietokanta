from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
import os

# using postgresql on heroku
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tea.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# application
from application import views

from application.tea import models as tea_models
from application.auth import models as auth_models
db.create_all()

from application.auth import views

# login
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään käyttääksesi tätä toimintoa."

@login_manager.user_loader
def load_user(user_id):
    return auth_models.User.query.get(user_id)

from application.tea import views

