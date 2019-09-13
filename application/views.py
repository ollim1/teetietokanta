from flask import render_template
from application import app
from application.tea import views

@app.route("/")
def index():
    return render_template("index.html")
