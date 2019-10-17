from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from application import app, db, bcrypt
from application.auth.models import User, Role
from application.auth.forms import LoginForm, AddUserForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm(), next = request.args.get("next"))
    else:
        form = LoginForm(request.form)

        user = User.query.filter_by(username=form.username.data).first()
        if not (user and bcrypt.check_password_hash(user.password_hash, form.password.data)):
            return render_template("auth/loginform.html", form = form,
                                   error = "Tarkista käyttäjänimi tai salasana.")

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
    else:
        form = AddUserForm(request.form)
        errors = []
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                user = User(form.name.data, form.username.data, bcrypt.generate_password_hash(form.password.data).decode("utf-8"))
                user.role = Role.query.filter_by(name="user").first().id
                db.session.add(user)
                db.session.commit()
                print("Käyttäjä %s luotu" % user.name)
                login_user(user)
            else:
                errors.append("Käyttäjänimi on jo käytössä.")
        else:
            errors.append("Tarkista lomakkeen tiedot.")
        if len(errors) > 0:
            return render_template("auth/add_user.html", form = form,
                                   errors = errors)
        return redirect(url_for("index"))
