from application import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

teaingredient = Table("tea_ingredient",
        db.Model.metadata,
        db.Column("tea", db.Integer, db.ForeignKey("tea.id"), primary_key=True),
        db.Column("ingredient", db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)
)

class BrewData(db.Model):
    __abstract__ = True

    temperature = db.Column(db.Float)
    brewtime = db.Column(db.Integer)
    boiled = db.Column(db.Boolean)

class Named(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)

class TeaType(Named):
    ingredients = relationship("Ingredient")
    def __init__(self, name):
        self.name = name

class Ingredient(Named):
    teatype = db.Column(db.Integer, db.ForeignKey('tea_type.id'))

    teas = db.relationship("Tea", secondary = teaingredient, back_populates = "ingredients")
    def __init__(self, name, teatype = None):
        self.name = name
        self.teatype = teatype

class Tea(BrewData, Named):
    ingredients = db.relationship("Ingredient", secondary = teaingredient, back_populates = "teas")
    reviews = db.relationship("Review")
    def __init__(self, name, temperature, brewtime, boiled):
        self.name = name
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled

    @classmethod
    def get_info(cls):
        stmt = text("SELECT ingredient.name, tea_type.name FROM tea_ingredient"
                + " JOIN ingredient ON ingredient.id = tea_ingredient.ingredient"
                + " LEFT JOIN tea_type ON tea_type.id = ingredient.teatype"
                + " WHERE tea_ingredient.tea = :tea").params(tea=self.id)
        res = db.engine.execute(stmt)
        ingredient_list = []
        for row in res:
            ingredient_list.append({"name":row[0], "teatype":row[1]})
        return {"tea":self, "ingredients":ingredient_list}

    @classmethod
    def list_teas(cls):
        stmt = text("SELECT tea.id, tea.name, AVG(review.score) FROM tea"
                + " LEFT JOIN review ON review.tea = tea.name")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "score":row[2]})
        return response

    @classmethod
    def selection_list(cls):
        response = []
        for row in Tea.list_teas():
            response.append((row["id"], row["name"]))

class User(Named):
    reviews = db.relationship("Review")
    def __init__(self, name):
        self.name = name

class Review(BrewData):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    tea = db.Column(db.Integer, db.ForeignKey('tea.id'))
    score = db.Column(db.Integer)
    content = db.Column(db.Text)

    def __init__(self, user, tea, score, content, temperature, brewtime, boiled):
        self.user = user
        self.tea = tea
        self.score = score
        self.content = content
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled
