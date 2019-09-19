from application import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

teaingredient = Table("tea_ingredient",
        db.Model.metadata,
        db.Column("tea", db.Integer, db.ForeignKey("tea.id"), primary_key=True),
        db.Column("ingredient", db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)
)

class TeaType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)

    ingredients = relationship("Ingredient")
    def __init__(self, name):
        self.name = name

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)
    teatype = db.Column(db.Integer, db.ForeignKey('tea_type.id'))

    teas = relationship("Tea", secondary = teaingredient, back_populates = "ingredients")
    def __init__(self, name, teatype = None):
        self.name = name
        if teatype:
            self.teatype = teatype.id

class Tea(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)
    temperature = db.Column(db.Float, nullable = False)
    brewtime = db.Column(db.Integer, nullable = False)
    boiled = db.Column(db.Boolean, nullable = False)

    ingredients = db.relationship("Ingredient", secondary = teaingredient, back_populates = "teas")
    def __init__(self, name, temperature, brewtime, boiled):
        self.name = name
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)

    def __init__(self, name):
        self.name = name

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    tea = db.Column(db.Integer, db.ForeignKey('tea.id'))
    content = db.Column(db.Text)
    temperature = db.Column(db.Float)
    brewtime = db.Column(db.Integer)
    boiled = db.Column(db.Boolean)

    def __init__(self, user, tea, content, temperature, brewtime, boiled):
        self.user = user
        if tea:
            self.tea = tea.id
        self.content = content
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled
