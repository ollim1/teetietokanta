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
