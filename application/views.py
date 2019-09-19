from flask import render_template
from flask_login import login_required, current_user, login_user
from application import app, db

@app.route("/")
def index():
    return render_template("index.html")
