from application import db
from application.tea.models import *
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

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

