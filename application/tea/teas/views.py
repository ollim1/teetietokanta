from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import current_user, login_user
from application import login_required
from flask import redirect, render_template, request, url_for
from application.tea.models import *
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm
from application.tea import views

@app.route("/tea/teas/list")
def teas_page():
    return render_template("tea/teas/list.html", teas = Tea.list_teas())

@app.route("/tea/teas/view")
def view_tea():
    id = request.args.get("id")
    if id:
        tea = db.session.query(Tea).get(id)
        if not tea:
            print("could not find tea: id " + str(id))
            abort(404)
        tea_info = tea.get_info()
        print(str(tea))
        print(str(tea.temperature))
        print(str(tea.brewtime))
        print(str(tea.boiled))
        return render_template("/tea/teas/view.html", tea = tea, teatype = tea_info["type"], ingredients = tea_info["ingredients"], reviews = Review.list(tea=tea.id))
    else:
        abort(404)

@app.route("/tea/teas/add", methods=["GET", "POST"])
@login_required()
def add_tea():
    if request.method == "GET":
        return render_template("tea/teas/add.html", form = TeaNameForm())
    if request.method == "POST":
        form = TeaNameForm(request.form)
        if form.validate_on_submit():
            name = form.name.data
            tea = Tea(name)
            db.session.add(tea)
            db.session.commit()
            return redirect(url_for("modify_tea", id = tea.id))
        else:
            return redirect(url_for("add_tea"))

@app.route("/tea/teas/modify", methods=["GET", "POST"])
@login_required()
def modify_tea():
    if request.method == "GET":
        id = request.args.get("id")
        if id:
            tea = db.session.query(Tea).get(id)
            if not tea:
                print("could not find tea: id " + str(id))
                abort(404)
            tea_info = tea.get_info()
            form = TeaModificationForm(data = {"name": tea.name, "temperature": tea.temperature, "brewtime": tea.brewtime, "boiled": tea.boiled, "type": tea.type})
            form.type.choices = TeaType.selection_list()
            return render_template("/tea/teas/modify.html",
                    form = form, tea = tea)
        else:
            abort(404)
    else:
        id = request.form.get("id") # input type "hidden", fill in using form parameters
        form = TeaModificationForm(request.form)
        name = form.name.data
        temperature = form.temperature.data
        brewtime = form.brewtime.data
        boiled = form.boiled.data
        type = form.type.data
        errors = []
        # FlaskForm's validate_on_submit randomly decided to stop working
        if len(name) < 1 or len(name) > 255:
            errors.append("Nimen pituuden on oltava välillä 1-255.")
        if not isinstance(temperature, float) or temperature < -10 or temperature > 110:
            errors.append("Lämpötilan on oltava välillä -10-110 °C")
        if not isinstance(brewtime, float) or brewtime < 0 or brewtime > 60:
            errors.append("Haudutusajan on oltava välillä 0-60 min")
        if not isinstance(brewtime, float) or brewtime < 0 or brewtime > 60:
            errors.append("Haudutusajan on oltava välillä 0-60 min")
        if int(type) < 1:
            # could not figure out how to get query row count efficiently with just orm, may explode
            if int(type) == -1:
                type = None
            else:
                errors.append("Virheellinen teetyypin indeksi.")
        if len(errors) > 0:
            return redirect(url_for("modify_tea", id = id))
        print(errors)
        tea = db.session.query(Tea).get(id)
        tea.name = name
        tea.temperature = temperature
        tea.brewtime = brewtime
        tea.boiled = boiled
        tea.type = type
        db.session.commit()
        return redirect(url_for("view_tea", id = id))

@app.route("/tea/teas/delete", methods=["POST"])
@login_required(role="admin")
def delete_tea():
    id = request.form.get("id")
    tea = db.session.query(Tea).get(id)
    if not tea:
        return abort(404)
    ingredients = tea.ingredients
    for ingredient in ingredients:
        ingredient.teas.remove(tea)
    db.session.delete(tea)
    db.session.commit()
    return redirect(url_for("teas_page"))

@app.route("/tea/teas/add_ingredient", methods=["GET", "POST"])
@login_required()
def add_ingredient_to_tea():
    if request.method == "GET":
        id = request.args.get("id")
        tea = db.session.query(Tea).get(id)
        if not tea:
            return abort(404)
        form = AddIngredientToTeaForm()
        form.ingredient.choices=Ingredient.selection_list()
        return render_template("tea/teas/add_ingredient.html", id = id, form = form, tea = tea, ingredients = tea.get_info()["ingredients"])
    else:
        id = request.form.get("id")
        ingredient_id = request.form.get("ingredient")
        if not id:
            return abort(404)
        if not ingredient_id:
            return redirect(url_for("add_ingredient_to_tea", id = id))
        ingredient_id = int(ingredient_id)
        if ingredient_id != -1:
            tea = db.session.query(Tea).get(id)
            print("\n\n\nid: " + str(id) + ", ingredient_id: " + str(ingredient_id) + "\n\n\n")
            ingredient = db.session.query(Ingredient).get(ingredient_id)
            tea.ingredients.append(ingredient)
            db.session.commit()
        else:
            print("\n\n\nfailed to add ingredient: id: " + str(id) + ", ingredient_id: " + str(ingredient_id) + "\n\n\n")
        return redirect(url_for("add_ingredient_to_tea", id = id))

