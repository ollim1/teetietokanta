from application import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, validators
from flask import redirect, render_template, request, url_for
from application.tea.models import *

class AddTeaTypeForm(FlaskForm):
    name = StringField("Teetyyppi", [validators.Length(min=1)])

    class Meta:
        csrf = False

class AddIngredientForm(FlaskForm):
    name = StringField("Ainesosa", [validators.Length(min=1)])

    class Meta:
        csrf = False

@app.route("/tea/ingredients")
def ingredients_page():
    return render_template("ingredients.html",
        ingredients = db.session.query(Ingredient, TeaType)
                                .outerjoin(TeaType).all(),
        teatypes = TeaType.query.all())

@app.route("/tea/teatypes")
def teatypes_page():
    return render_template("teatypes.html", teatypes = TeaType.query.all())

@app.route("/tea/add_teatype", methods=["GET", "POST"])
def add_teatype():
    if request.method == "POST":
        name = request.form.get("name")
        if not TeaType.query.filter_by(name=name).first():
            teatype = TeaType(name)
            db.session.add(teatype)
            db.session.commit()
        return redirect(url_for("teatypes_page"))
    else:
        return render_template("add_teatype.html", form = AddTeaTypeForm())

@app.route("/tea/modify_ingredient", methods=["POST"])
def modify_ingredient():
    ingredient_id = int(request.form.get("ingredient_id"))
    teatype_id = int(request.form.get("teatype_id"))
    ingredient = db.session.query(Ingredient).get(ingredient_id)
    if teatype_id != -1:
        ingredient.teatype = teatype_id
    else:
        ingredient.teatype = None
    db.session.commit()
    return redirect(url_for("ingredients_page"))

@app.route("/tea/add_ingredient", methods=["GET", "POST"])
def add_ingredient():
    if request.method == "POST":
        name = request.form.get("name")
        teatype = request.form.get("teatype_id")
        if teatype == -1:
            i = Ingredient(name)
        else:
            i = Ingredient(name, teatype)
        db.session.add(i)
        db.session.commit()
        return redirect(url_for("ingredients_page"))
    else:
        return render_template("add_ingredient.html", form = AddIngredientForm(), teatypes = TeaType.query.all())
