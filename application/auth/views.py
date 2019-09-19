from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, AddUserForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Tarkista käyttäjänimi tai salasana")

    print("Käyttäjä " + user.name + " tunnistettiin")
    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/add_user", methods = ["GET", "POST"])
def auth_add_user():
    if request.method == "GET":
        return render_template("auth/add_user.html", form = AddUserForm())

    form = AddUserForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template("auth/add_user.html", form = form,
                               error = "Käyttäjänimi on jo käytössä")

    user = User(form.name.data, form.username.data, form.password.data)
    db.session.add(user)
    db.session.commit()
    print("Käyttäjä " + user.name + " luotu")
    login_user(user)
    return redirect(url_for("index"))
