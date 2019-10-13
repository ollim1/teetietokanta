from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from application import app, db
from application.auth.models import User, Role
from application.auth.forms import LoginForm, AddUserForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm(), next = request.args.get("next"))

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Tarkista käyttäjänimi tai salasana")

    print("Käyttäjä %s tunnistettiin" % user.name)
    login_user(user)
    return redirect(request.form.get("next") or url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/add_user", methods = ["GET", "POST"])
def auth_add_user():
    if request.method == "GET":
        return render_template("auth/add_user.html", form = AddUserForm())

    form = AddUserForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            return render_template("auth/add_user.html", form = form,
                                   error = "Käyttäjänimi on jo käytössä")

        user = User(form.name.data, form.username.data, form.password.data)
        user.role = Role.query.filter_by(name="user").first().id
        db.session.add(user)
        db.session.commit()
        print("Käyttäjä %s luotu" % user.name)
        login_user(user)
    else:
        print("validation failed")
        return render_template("auth/add_user.html", form = form, error = "Salasanojen on oltava sama")
    return redirect(url_for("index"))
