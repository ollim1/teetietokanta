from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import login_required, current_user, login_user
from flask import redirect, render_template, request, url_for
from application.tea.models import TeaType, Ingredient, Tea, User, Review
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm

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
            Flask.abort(400)
        tea_info = tea.get_info()
        return render_template("/tea/modify_tea_form.html", form = TeaModificationForm(data = {"name": tea.name, "temperature": tea.temperature, "brewtime": tea.brewtime, "boiled": tea.boiled}), tea_info = tea_info)
    else:
        Flask.abort(400)

@app.route("/tea/modify_tea", methods=["POST"])
@login_required
def modify_tea():
    id = request.form.get("id") # input type "hidden", fill in using form parameters
    name = request.form.get("name")
    temperature = request.form.get("temperature")
    brewtime = request.form.get("brewtime")
    boiled = request.form.get("boiled")
    ingredient_id = request.form.get("ingredient_id")
    # tea = db.session.query(Tea).get(id)
    # TODO: add database logic including the adding of ingredients
    return redirect(url_for("teas_page"))

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
