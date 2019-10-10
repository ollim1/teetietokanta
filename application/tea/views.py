from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import current_user, login_user
from application import login_required
from flask import redirect, render_template, request, url_for
from application.tea.models import *
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm

@app.route("/tea/ingredients/list")
def ingredients_page():
    return render_template("tea/ingredients/list.html", ingredients = Ingredient.query.all())

@app.route("/tea/ingredients/add", methods=["GET", "POST"])
@login_required()
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

@app.route("/tea/reviews/add", methods=["GET", "POST"])
@login_required()
def add_review():
    if request.method == "GET":
        id = request.args.get("id")
        if not id:
            abort(404)
        tea = db.session.query(Tea).get(id)
        if not tea:
            abort(404)
        print("tea is " + str(id))
        return render_template("tea/reviews/add.html", id = id, form = ReviewForm(data = {
            "name": tea.name,
            "temperature": tea.temperature,
            "brewtime": tea.brewtime,
            "boiled": tea.boiled,
            "score": 5,
            "type": tea.type}),
            tea = tea)
    else:
        id = request.form.get("id")
        score = request.form.get("score")
        text = request.form.get("text")
        add_brewinfo = request.form.get("add_brewinfo") == "y"
        review = None
        if add_brewinfo:
            temperature = request.form.get("temperature")
            brewtime = request.form.get("brewtime")
            boiled = request.form.get("boiled") == "y"
            review = Review(user = current_user.id, tea = id, score = int(score), content = text, temperature = temperature, brewtime = brewtime, boiled = boiled)
        else:
            review = Review(user = current_user.id, tea = id, score = int(score), content = text, temperature = None, brewtime = None, boiled = None)
        print("current_user is " + str(current_user.id))
        print("tea is " + str(id))
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("teas_page"))

# TODO: implement listing and editing of reviews

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
        return render_template("/tea/teas/view.html", tea = tea, teatype = tea_info["type"], ingredients = tea_info["ingredients"])
    else:
        abort(404)

@app.route("/tea/teas/add", methods=["GET", "POST"])
@login_required()
def add_tea():
    if request.method == "GET":
        return render_template("tea/teas/add.html", form = TeaNameForm())
    if request.method == "POST":
        name = request.form.get("name")
        tea = Tea(name)
        db.session.add(tea)
        db.session.commit()
        return redirect(url_for("modify_tea", id = tea.id))

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
        name = request.form.get("name")
        temperature = request.form.get("temperature")
        brewtime = request.form.get("brewtime")
        boiled = request.form.get("boiled") == "y"
        type = int(request.form.get("type"))
        tea = db.session.query(Tea).get(id)
        tea.name = name
        tea.temperature = temperature
        tea.brewtime = brewtime
        tea.boiled = boiled
        if type != -1:
            tea.type = type
        db.session.commit()
        return redirect(url_for("view_tea", id = id))

@app.route("/tea/teas/delete", methods=["POST"])
@login_required()
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
            print("\n\n\nid: " + str(id) + ", ingredient_id: " + ingredient_id + "\n\n\n")
            ingredient = db.session.query(Ingredient).get(ingredient_id)
            tea.ingredients.append(ingredient)
            db.session.commit()
        else:
            print("\n\n\nfailed to add ingredient: id: " + str(id) + ", ingredient_id: " + str(ingredient_id) + "\n\n\n")
        return redirect(url_for("add_ingredient_to_tea", id = id))

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
    id = int(request.args.get(id))
    teatype = db.session.query.get(id)
    if not teatype:
        return error(404)
    for tea in teatype.teas:
        tea.teatype = None
    db.session.commit()
    return render_template("tea/teatypes/list.html")

@app.route("/tea/teatypes/modify", methods=["POST"])
@login_required(role="admin")
def modify_teatype():
    id = int(request.args.get("id"))
    name = request.args.get("name")
    teatype = db.session.query.get(id)
    if not teatype:
        return error(404)
    teatype.name = name
    db.session.commit()
    return render_template("tea/teatypes/list.html")
