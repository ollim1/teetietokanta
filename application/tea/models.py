from application import db
from application.auth.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

teaingredient = Table("tea_ingredient",
        db.Model.metadata,
        db.Column("tea", db.Integer, db.ForeignKey("tea.id"), primary_key=True),
        db.Column("ingredient", db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)
)

class BrewData(db.Model):
    # TODO: normalize
    __abstract__ = True

    temperature = db.Column(db.Float)
    brewtime = db.Column(db.Float)
    boiled = db.Column(db.Boolean)

class Named(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)

class TeaType(Named):
    # TODO: type-specific default brewing information
    teas = relationship("Tea")
    def __init__(self, name):
        self.name = name

    @staticmethod
    def selection_list():
        stmt = text("SELECT id, name FROM tea_type")
        res = db.engine.execute(stmt).fetchall()
        response = []
        response.append((-1, "Tyhjä"))
        for row in res:
            response.append((row["id"], row["name"]))
        return response

class Ingredient(Named):
    teas = db.relationship("Tea", secondary = teaingredient, back_populates = "ingredients")
    def __init__(self, name):
        self.name = name

    @staticmethod
    def selection_list():
        stmt = text("SELECT id, name FROM ingredient")
        res = db.engine.execute(stmt).fetchall()
        response = []
        response.append((-1, "Tyhjä"))
        for row in res:
            response.append((row["id"], row["name"]))
        return response

class Tea(BrewData, Named):
    ingredients = db.relationship("Ingredient", secondary = teaingredient, back_populates = "teas")
    reviews = db.relationship("Review")
    type = db.Column(db.Integer, db.ForeignKey('tea_type.id'))

    def __init__(self, name, temperature = 100, brewtime = 3, boiled = True):
        self.name = name
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled

    def get_info(self):
        stmt = text("SELECT ingredient.id, ingredient.name FROM tea_ingredient"
                + " JOIN ingredient ON ingredient.id = tea_ingredient.ingredient"
                + " WHERE tea_ingredient.tea = :tea").params(tea=self.id)
        res = db.engine.execute(stmt)
        ingredient_list = []
        for row in res:
            ingredient_list.append({"id":row[0], "name":row[1]})
        type = None
        if self.type:
            type = db.session.query(TeaType).get(self.type)
            if type:
                type = type.name
        return {"tea":self, "type":type, "ingredients":ingredient_list}

    @staticmethod
    def list_teas():
        stmt = text("SELECT tea.id, tea.name, tea_type.name, AVG(review.score) as average FROM tea"
                + " LEFT JOIN tea_type ON tea_type.id = tea.type"
                + " LEFT JOIN review ON review.tea = tea.id"
                + " GROUP BY tea.id, tea_type.name"
                + " ORDER BY average DESC")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "type":row[2], "score":row[3]})
        return response

    @staticmethod
    def selection_list():
        stmt = text("SELECT tea.id, tea.name FROM tea")
        res = db.engine.execute(stmt).fetchall()
        response = []
        response.append((-1, "Tyhjä"))
        for row in res:
            response.append((row["id"], row["name"]))
        return response

class Review(BrewData):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'))
    tea = db.Column(db.Integer, db.ForeignKey('tea.id'))
    score = db.Column(db.Integer)
    content = db.Column(db.Text)

    def __init__(self, user, tea, score, content, temperature = None, brewtime = None, boiled = None):
        self.user = user
        self.tea = tea
        self.score = score
        self.content = content
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled
