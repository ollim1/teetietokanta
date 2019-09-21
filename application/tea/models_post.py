from application import db
from sqlalchemy.sql import text
from application.tea.models import *

def get_info(self):
    stmt = text("SELECT ingredient.name, tea_type.name FROM tea_ingredient"
            + " JOIN ingredient ON ingredient.id = tea_ingredient.ingredient"
            + " LEFT JOIN tea_type ON tea_type.id = ingredient.teatype"
            + " WHERE tea_ingredient.tea = :tea").params(tea=self.id)
    res = db.engine.execute(stmt)
    ingredient_list = []
    for row in res:
        ingredient_list.append({"name":row[0], "teatype":row[1]})
    return {"tea":self, "ingredients":ingredient_list}
setattr(Tea, "get_info", get_info)

def list_teas():
    stmt = text("SELECT tea.id, tea.name, AVG(review.score) FROM tea"
            + " LEFT JOIN review ON review.tea = tea.name")
    res = db.engine.execute(stmt)
    response = []
    for row in res:
        response.append({"id":row[0], "name":row[1], "score":row[2]})
    return response
setattr(Tea, "list_teas", staticmethod(list_teas))

def selection_list():
    response = []
    for row in Tea.list_teas():
        response.append((row["id"], row["name"]))
setattr(Tea, "selection_list", staticmethod(selection_list))

