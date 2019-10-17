from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import current_user, login_user
from application import login_required
from flask import redirect, render_template, request, url_for
from application.tea.models import *
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm

@app.route("/tea/ingredients/list")
def ingredients_page(errors = []):
    return render_template("tea/ingredients/list.html", ingredients = Ingredient.query.all(), errors = errors)

@app.route("/tea/ingredients/add", methods=["GET", "POST"])
@login_required()
def add_ingredient(errors = []):
    if request.method == "POST":
        form = IngredientForm(request.form)
        errors = []
        if form.validate_on_submit():
            name = form.name.data
            if not Ingredient.query.filter_by(name=name).first():
                ingredient = Ingredient(name)
                db.session.add(ingredient)
                db.session.commit()
            else:
                errors.append("Ainesosa on jo olemassa.")
        else:
            errors.append("Nimen pituuden on oltava välillä 1-255.")
        if len(errors) > 0:
            return render_template("tea/ingredients/add.html", form = IngredientForm(), errors = errors)
        return redirect(url_for("ingredients_page"))
    else:
        return render_template("tea/ingredients/add.html", form = IngredientForm(), errors = errors)

@app.route("/tea/ingredients/modify", methods=["POST"])
@login_required(role="admin")
def modify_ingredient():
    id = int(request.form.get("id"))
    name = request.form.get("name")
    ingredient = db.session.query(TeaType).get(id)
    if not name or len(name) < 1 or len(name) > 255:
        return render_template("tea/ingredients/list.html", ingredients = Ingredient.query.all(), errors = ["Nimen pituuden on oltava välillä 1-255."])
    if not ingredient:
        return abort(404)
    ingredient.name = name
    db.session.commit()
    return redirect(url_for("ingredients_page"))

@app.route("/tea/ingredients/delete", methods=["GET"])
@login_required(role="admin")
def delete_ingredient():
    id = int(request.args.get("id"))
    ingredient = db.session.query(Ingredient).get(id)
    if not ingredient:
        return abort(404)
    for tea in ingredient.teas:
        tea.ingredients.remove(ingredient)
    db.session.delete(ingredient)
    db.session.commit()
    return render_template("tea/ingredients/list.html", ingredients = Ingredient.query.all())
