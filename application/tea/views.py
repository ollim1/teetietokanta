from application import app, db
from flask import redirect, render_template, request, url_for
from application.tea.models import *

temp_list = ["musta tee", "vihreä tee", "valkoinen tee"]

@app.route("/ingredients")
def ingredients_page():
    return render_template("ingredients.html", ingredients = Ingredient.query.all())

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    name = request.form.get("name")
    teatype = request.form.get("teatype")
    if not teatype:
        i = Ingredient(name)
    else:
        i = Ingredient(name, teatype)
    db.session.add(i)
    db.session.commit()
    print("added " + Ingredient.name + " to db")
    return redirect(url_for("ingredients_page"))
