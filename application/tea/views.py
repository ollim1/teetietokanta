from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import login_required, current_user, login_user
from flask import redirect, render_template, request, url_for
from application.tea.models import TeaType, Ingredient, Tea, User, Review
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm

@app.route("/tea/teas")
def teas_page():
    return render_template("tea/teas.html", teas = Tea.list_teas())

@app.route("/tea/add_tea", methods=["GET", "POST"])
@login_required
def add_tea():
    if request.method == "GET":
        return render_template("tea/add_tea.html", form = TeaNameForm())
    if request.method == "POST":
        name = request.form.get("name")
        tea = Tea(name)
        db.session.add(tea)
        db.session.commit()
        return redirect(url_for("modify_tea_form", id = tea.id))

@app.route("/tea/modify_tea_form", methods=["GET"])
@login_required
def modify_tea_form():
    id = request.args.get("id")
    if id:
        tea = db.session.query(Tea).get(id)
        if not tea:
            print("could not find tea: id " + str(id))
            abort(404)
        tea_info = tea.get_info()
        return render_template("/tea/modify_tea_form.html", form = TeaModificationForm(data = {"name": tea.name, "temperature": tea.temperature, "brewtime": tea.brewtime, "boiled": tea.boiled}), tea = tea, ingredients = tea_info["ingredients"])
    else:
        abort(404)

@app.route("/tea/modify_tea", methods=["POST"])
@login_required
def modify_tea():
    id = request.form.get("id") # input type "hidden", fill in using form parameters
    name = request.form.get("name")
    temperature = request.form.get("temperature")
    brewtime = request.form.get("brewtime")
    boiled = request.form.get("boiled") == "y"
    ingredient_id = request.form.get("ingredient_id")
    tea = db.session.query(Tea).get(id)
    tea.name = name
    tea.temperature = temperature
    tea.brewtime = brewtime
    tea.boiled = boiled
    db.session.commit()
    return redirect(url_for("modify_tea_form", id = id))

@app.route("/tea/add_ingredient_to_tea", methods=["GET", "POST"])
@login_required
def add_ingredient_to_tea():
    if request.method == "GET":
        id = request.args.get("id")
        print("\n\n\nid: " + id + "\n\n\n")
        tea = db.session.query(Tea).get(id)
        if not tea:
            return abort(404)
        return render_template("tea/add_ingredient_to_tea.html", id = id, form = AddIngredientToTeaForm(), tea = tea, ingredients = tea.get_info()["ingredients"])
    else:
        id = request.form.get("id")
        ingredient_id = request.form.get("ingredient")
        if id and ingredient_id and ingredient_id != -1:
            tea = db.session.query(Tea).get(id)
            ingredient = db.session.query(Ingredient).get(ingredient_id)
            
            tea.ingredients.append(ingredient)
            print("\n\n\ndoing something\n\n\n")
            db.session.commit()
        else:
            print("id: " + str(id) + ", ingredient_id: " + ingredient_id)
        return redirect(url_for("add_ingredient_to_tea", id = id))

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
