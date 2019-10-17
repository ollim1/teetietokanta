from application import db
from application.auth.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from application.tea.base import *

teaingredient = Table("tea_ingredient",
        db.Model.metadata,
        db.Column("tea", db.Integer, db.ForeignKey("tea.id"), primary_key=True),
        db.Column("ingredient", db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)
)

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

class Review(BrewData, Timestamped):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'))
    title = db.Column(db.String(256))
    tea = db.Column(db.Integer, db.ForeignKey('tea.id'))
    score = db.Column(db.Integer)
    content = db.Column(db.Text)

    def __init__(self, user, title, tea, score, content, temperature = None, brewtime = None, boiled = None):
        self.user = user
        self.tea = tea
        self.title = title
        self.score = score
        self.content = content
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled

    @staticmethod
    def list(user = None, tea = None):
        if user:
            if tea:
                stmt = text("SELECT tea.id, tea.name, review.id, review.title, review.score FROM review"
                          + " JOIN tea ON tea.id = review.tea"
                          + " WHERE review.user = :user"
                          + " AND review.tea = :tea"
                          + " ORDER BY score DESC").params(user=user, tea=tea)
            else:
                stmt = text("SELECT tea.id, tea.name, review.id, review.title, review.score FROM review"
                          + " JOIN tea ON tea.id = review.tea"
                          + " WHERE review.user = :user"
                          + " ORDER BY score DESC").params(user=user)
        elif tea:
            stmt = text("SELECT tea.id, tea.name, review.id, review.title, review.score FROM review"
                      + " JOIN tea ON tea.id = review.tea"
                      + " WHERE review.tea = :tea"
                      + " ORDER BY score DESC").params(tea=tea)
        else:
            stmt = text("SELECT tea.id, tea.name, review.id, review.title, review.score FROM review"
                      + " JOIN tea ON tea.id = review.tea"
                      + " ORDER BY score DESC")
        res = db.engine.execute(stmt)
        ret = []
        for row in res:
            ret.append({"tea":{"id":row[0], "name":row[1]}, "review":{"id":row[2], "title":row[3], "score":row[4]}})
        return ret

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
        res = db.engine.execute(stmt).fetchall()
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
    
    @classmethod
    def count_unreviewed(cls):
        list = cls.list_unreviewed()
        return len(list)

    @staticmethod
    def list_unreviewed():
        stmt = text("select tea.id, tea.name from tea left join review on review.tea = tea.id where review.id is NULL")
        res = db.engine.execute(stmt).fetchall()
        response = []
        for row in res:
            response.append((row["id"], row["name"]))
        return response

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

