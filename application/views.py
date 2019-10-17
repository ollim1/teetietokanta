from flask import render_template
from flask_login import login_required, current_user, login_user
from application import app, db
from application.tea.models import Tea

@app.route("/")
def index():
    return render_template("index.html", unreviewed_count = Tea.count_unreviewed())
