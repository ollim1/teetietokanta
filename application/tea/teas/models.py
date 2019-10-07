from application import db
from application.tea.models import *
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

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
