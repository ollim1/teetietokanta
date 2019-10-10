from application import db
from application.tea.models import *
from application.tea.teatypes.models import *
from application.tea.reviews.models import *
from application.tea.teas.models import *
from application.tea.ingredients.models import *
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, PrimaryKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

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

