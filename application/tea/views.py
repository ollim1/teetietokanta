from application import app
from flask import redirect, render_template, request, url_for

temp_list = ["musta tee", "vihreä tee", "valkoinen tee"]

@app.route("/ingredients")
def ingredients_page():
    return render_template("ingredients.html", ingredients = temp_list)

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    print("added ingredient " + request.form.get("name"))
    return redirect(url_for("ingredients_page"))
