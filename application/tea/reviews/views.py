from application import app, db
from flask import abort
from flask_wtf import FlaskForm
from flask_login import current_user, login_user
from application import login_required
from flask import redirect, render_template, request, url_for
from application.tea.forms import TeaTypeForm, IngredientForm, BrewDataForm, ReviewForm, TeaNameForm, TeaModificationForm, AddIngredientToTeaForm
from application.tea import views
from application.tea.models import *

@app.route("/tea/reviews/list")
@login_required()
def reviews_page():
    reviews = Review.list(user = current_user.id)
    return render_template("tea/reviews/list.html", reviews = reviews)

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
        print("tea is %d", id)
        return render_template("tea/reviews/add.html", id = id, form = ReviewForm(data = {
            "name": tea.name,
            "temperature": tea.temperature,
            "brewtime": tea.brewtime,
            "boiled": tea.boiled,
            "score": 5}),
            tea = tea)
    else:
        form = ReviewForm(request.form)
        id = request.form.get("id")
        score = form.score.data
        title = form.title.data
        text = form.text.data
        add_brewinfo = form.add_brewinfo.data
        review = None
        if add_brewinfo:
            temperature = request.form.get("temperature")
            brewtime = request.form.get("brewtime")
            boiled = request.form.get("boiled") == "y"
            review = Review(user = current_user.id, title = title, tea = id, score = int(score), content = text, temperature = temperature, brewtime = brewtime, boiled = boiled)
        else:
            review = Review(user = current_user.id, title = title,  tea = id, score = int(score), content = text, temperature = None, brewtime = None, boiled = None)
        print("current_user is %s" % current_user.id)
        print("tea is " + str(id))
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("teas_page"))

# TODO: implement listing and editing of reviews
