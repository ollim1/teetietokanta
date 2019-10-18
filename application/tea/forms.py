from application import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, TextAreaField, FloatField, BooleanField, validators
from application.tea.models import TeaType, Ingredient, Tea, User, Review

class TeaTypeForm(FlaskForm):
    name = StringField("Teetyyppi", [validators.Length(min=1, max=255)])

    class Meta:
        csrf = False

class IngredientForm(FlaskForm):
    name = StringField("Ainesosa", [validators.Length(min=1, max=255)])

    class Meta:
        csrf = False

class BrewDataForm(FlaskForm):
    __abstract__ = True
    temperature = FloatField("Lämpötila", [validators.InputRequired(), validators.NumberRange(min=-10, max=110)])
    brewtime = FloatField("Haudutuksen pituus (min)", [validators.NumberRange(min=0, max=60), validators.InputRequired()])
    boiled = BooleanField("Keitetty")

    class Meta:
        csrf = False

class ReviewForm(BrewDataForm):
    score = RadioField("Arvosana", [validators.Optional()], choices = [(1, "★"), (2, "★★"), (3, "★★★"), (4, "★★★★"), (5, "★★★★★")])
    title = StringField("Otsikko", [validators.Length(min=1, max=255)])
    text = TextAreaField("Teksti")
    add_brewinfo = BooleanField("Lisää haudutustiedot", default = "unchecked")

    class Meta:
        csrf = False

class TeaNameForm(FlaskForm):
    """
    Using a basic name form to create an initial object to fill in before committing to the tea table.
    """
    name = StringField("Nimi", [validators.Length(min=1, max=255)])

    class Meta:
        csrf = False

class TeaModificationForm(BrewDataForm):
    """
    Used for both filling out the initial information and modifying it later.
    """
    name = StringField("Nimi", [validators.Length(min=1, max=255)])
    type = SelectField("Teetyyppi")

    class Meta:
        csrf = False

class AddIngredientToTeaForm(FlaskForm):
    ingredient = SelectField("Tee", [validators.InputRequired(), validators.Length(min=1, max=255)])

    class Meta:
        csrf = False
