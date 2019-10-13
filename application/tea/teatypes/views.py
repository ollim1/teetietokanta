from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import current_user, login_user
from application import login_required
from flask import redirect, render_template, request, url_for
from application.tea.models import *
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm
from application.tea import views

@app.route("/tea/teatypes/list")
def teatypes_page():
    return render_template("tea/teatypes/list.html", teatypes = TeaType.query.all())

@app.route("/tea/teatypes/add", methods=["GET", "POST"])
@login_required()
def add_teatype():
    if request.method == "POST":
        name = request.form.get("name")
        if not TeaType.query.filter_by(name=name).first():
            teatype = TeaType(name)
            db.session.add(teatype)
            db.session.commit()
        return redirect(url_for("teatypes_page"))
    else:
        return render_template("tea/teatypes/add.html", form = TeaTypeForm())

@app.route("/tea/teatypes/delete", methods=["GET"])
@login_required(role="admin")
def delete_teatype():
    id = int(request.args.get("id"))
    teatype = db.session.query(TeaType).get(id)
    if not teatype:
        return error(404)
    for tea in teatype.teas:
        tea.teatype = None
    db.session.delete(teatype)
    db.session.commit()
    return render_template("tea/teatypes/list.html")

@app.route("/tea/teatypes/modify", methods=["POST"])
@login_required(role="admin")
def modify_teatype():
    id = int(request.form.get("id"))
    name = request.form.get("name")
    teatype = db.session.query(TeaType).get(id)
    if not name or length(name) < 1 or length(name) > 255:
        return render_template("tea/teatypes/list.html",
                error = "Uusi nimi on liian pitkä tai lyhyt",
                teatypes = TeaType.query.all())
    if not teatype:
        return error(404)
    teatype.name = name
    db.session.commit()
    return render_template("tea/teatypes/list.html")

