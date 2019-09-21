from application import app, db
from flask_wtf import FlaskForm
from flask_login import login_required, current_user, login_user
from wtforms import StringField, SelectField, RadioField, TextAreaField, FloatField, BooleanField, validators
from flask import redirect, render_template, request, url_for
from application.tea.models import *

class TeaTypeForm(FlaskForm):
    name = StringField("Teetyyppi", [validators.Length(min=1)])

    class Meta:
        csrf = False

class IngredientForm(FlaskForm):
    name = StringField("Ainesosa", [validators.Length(min=1)])

    class Meta:
        csrf = False

class ReviewForm(FlaskForm):
    tea = SelectField("Tee", [validators.InputRequired()], choices=Tea.selection_list())
    score = RadioField("Arvosana", [validators.InputRequired()], choices = [("★", 1), ("★★", 2), ("★★★", 3), ("★★★★", 4), ("★★★★★", 5)])
    text = TextAreaField("Teksti")
    temperature = FloatField("Lämpötila", [validators.InputRequired()])
    brewtime = FloatField("Haudutuksen pituus (min)", [validators.NumberRange(min=0), validators.InputRequired()])
    boiled = BooleanField("Keitetty", default="checked")

@app.route("/tea/teas")
def teas_page():
    return render_template("teas.html", teas = list_teas())

@app.route("/tea/ingredients")
def ingredients_page():
    return render_template("tea/ingredients.html",
        ingredients = db.session.query(Ingredient, TeaType)
                                .outerjoin(TeaType).all(),
        teatypes = TeaType.query.all())

@app.route("/tea/teatypes")
def teatypes_page():
    return render_template("tea/teatypes.html", teatypes = TeaType.query.all())

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
        return render_template("tea/add_teatype.html", form = TeaTypeForm())

@app.route("/tea/modify_ingredient", methods=["POST"])
@login_required
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
@login_required
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
        return render_template("tea/add_ingredient.html", form = IngredientForm(), teatypes = TeaType.query.all())
