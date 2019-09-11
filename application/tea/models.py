from application import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

class Type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, name):
        self.name = name

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)

    def __init__(self, name):
        self.name = name
