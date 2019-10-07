from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import login_required, current_user, login_user
from flask import redirect, render_template, request, url_for
from application.tea.models import TeaType, Ingredient, Tea, User, Review
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm

@app.route("/tea/teatypes")
def teatypes_page():
    return render_template("tea/teatypes/list.html", teatypes = TeaType.query.all())

@app.route("/tea/add_teatype", methods=["GET", "POST"])
@login_required
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
