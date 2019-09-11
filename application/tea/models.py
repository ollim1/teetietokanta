from application import db

class Ingredient(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

class Type(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, name):
        self.name = name

class User(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

class Review(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(512), nullable=False)

    def __init__(self, name):
        self.name = name
