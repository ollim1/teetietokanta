from application import app
from flask import render_template, request

@app.route("/tea/newtea/")
def tea_form():
    return render_template("tea/newtea.html")

@app.route("/tea/")
def tea_create():
    print(request.form.get("name"))
