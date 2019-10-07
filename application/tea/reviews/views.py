from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import login_required, current_user, login_user
from flask import redirect, render_template, request, url_for
from application.tea.models import TeaType, Ingredient, Tea, User, Review
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm

@app.route("/tea/reviews/add", methods=["GET", "POST"])
@login_required
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
