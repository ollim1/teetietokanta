from application import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, TextAreaField, FloatField, BooleanField, validators
from application.tea.models import TeaType, Ingredient, Tea, User, Review

class TeaTypeForm(FlaskForm):
    name = StringField("Teetyyppi", [validators.Length(min=1)])

    class Meta:
        csrf = False

class IngredientForm(FlaskForm):
    name = StringField("Ainesosa", [validators.Length(min=1)])

    class Meta:
        csrf = False

class BrewDataForm(FlaskForm):
    __abstract__ = True
    temperature = FloatField("Lämpötila", [validators.InputRequired()], default = 100)
    brewtime = FloatField("Haudutuksen pituus (min)", [validators.NumberRange(min=0), validators.InputRequired()], default = 3)
    boiled = BooleanField("Keitetty")

    class Meta:
        csrf = False

class ReviewForm(BrewDataForm):
    tea = SelectField("Tee", [validators.InputRequired()], choices=Tea.query.all())
    score = RadioField("Arvosana", [validators.InputRequired()], choices = [("★", 1), ("★★", 2), ("★★★", 3), ("★★★★", 4), ("★★★★★", 5)])
    text = TextAreaField("Teksti")

    class Meta:
        csrf = False

class TeaNameForm(FlaskForm):
    """
    Using a basic name form to create an initial object to fill in before committing to the tea table.
    """
    name = StringField("Nimi", [validators.Length(min=1)])

    class Meta:
        csrf = False

class TeaModificationForm(BrewDataForm, ):
    """
    Used for both filling out the initial information and modifying it later.
    """
    name = StringField("Nimi", [validators.Length(min=1)])

    class Meta:
        csrf = False