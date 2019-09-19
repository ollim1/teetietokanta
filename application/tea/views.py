from application import app, db
from flask import redirect, render_template, request, url_for
from application.tea.models import *

@app.route("/ingredients")
def ingredients_page():
    return render_template("ingredients.html", ingredients = Ingredient.query.all())

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    name = request.form.get("name")
    teatype_id = request.form.get("teatype_id")
    teatype_name = request.form.get("teatype_name")
    teatype = None
    if teatype_id != "-1":
        teatype = TeaType.query.get(teatype_id)
        print("Found TeaType: " + str(teatype.name))
    elif len(teatype_name) > 0:
        teatype = TeaType.query.filter_by(name=teatype_name).first()
        if not teatype:
            teatype = TeaType(teatype_name)
            db.session.add(teatype)
    if not teatype:
        i = Ingredient(name)
    else:
        i = Ingredient(name, teatype)
    db.session.add(i)
    db.session.commit()
    return redirect(url_for("ingredients_page"))
