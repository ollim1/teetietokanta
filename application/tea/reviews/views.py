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

@app.route("/tea/reviews/view")
def view_review():
    id = request.args.get("id")
    review = db.session.query(Review).get(id)
    if not review:
        return abort(404)
    tea = db.session.query(Tea).get(review.tea)
    return render_template("tea/reviews/view.html", review = review, tea = tea)
        
@app.route("/tea/reviews/modify", methods=["GET", "POST"])
@login_required()
def modify_review():
    if request.method == "GET":
        id = request.args.get("id")
        review = db.session.query(Review).get(id)
        if not review:
            return abort(404)
        if current_user and current_user.is_authenticated and current_user.id == review.user:
            return render_template("tea/reviews/modify.html", form=ReviewForm(data = {"score": review.score, "title":review.title, "text":review.text, "add_brewinfo":true, "temperature":review.temperature, "brewtime":review.brewtime, "boiled": review.boiled}), review = review)
        else:
            return error(503)
    else:
        return error(503)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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
        errors = []
        if score and (not is_int(score) or int(score) < 1 or int(score) > 5):
            errors.append("Arvosanan on oltava välillä 1-5.")
        if not title or len(title) < 1 or len(title) > 255:
            errors.append("Otsikon pituuden on oltava välillä 1-255.")
        temperature = None
        brewtime = None
        boiled = None
        if add_brewinfo:
            temperature = form.temperature.data
            brewtime = form.temperature.data
            boiled = form.boiled.data
        if temperature and (not is_float(temperature) or float(temperature) < -10 or float(temperature) > 110):
            errors.append("Lämpötilan on oltava välillä -10-110 °C.")
        else:
            temperature = float(temperature)
        if brewtime and (not is_float(brewtime) or float(brewtime) < -10 or float(brewtime) > 110):
            errors.append("Haudutusajan on oltava välillä 0-60 minuuttia.")
        else:
            brewtime = float(brewtime)

        if len(errors) > 0:
            print("validation failed, %d errors:" % len(errors))
            for error in errors:
                print(error)
            print("%r" % form.score.data)
            return redirect(url_for("add_review", id = id))
        else:
            if add_brewinfo:
                review = Review(user = current_user.id, title = title, tea = id, score = int(score), content = text, temperature = temperature, brewtime = brewtime, boiled = boiled)
            else:
                review = Review(user = current_user.id, title = title,  tea = id, score = int(score), content = text, temperature = None, brewtime = None, boiled = None)
            print("current_user is %s" % current_user.id)
            print("tea is " + str(id))
            db.session.add(review)
            db.session.commit()
        return redirect(url_for("teas_page"))

# TODO: implement listing and editing of reviews
