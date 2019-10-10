from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import login_required, current_user, login_user
from flask import redirect, render_template, request, url_for
from application.tea import models
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm

@app.route("/tea/ingredients")
def ingredients_page():
    return render_template("tea/ingredients/list.html", ingredients = Ingredient.query.all())

@app.route("/tea/add_ingredient", methods=["GET", "POST"])
@login_required
def add_ingredient():
    if request.method == "POST":
        form = IngredientForm(request.form)
        name = form.name.data
        if not Ingredient.query.filter_by(name=name).first():
            ingredient = Ingredient(name)
            db.session.add(ingredient)
            db.session.commit()
        return redirect(url_for("ingredients_page"))
    else:
        return render_template("tea/ingredients/add.html", form = IngredientForm())
