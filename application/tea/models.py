from application import db

class Tea(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    brewtime = db.Column(db.Integer, nullable=False)
    boiled = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, temperature, brewtime, boiled):
        self.name = name
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable=False)

    def __init__(self, name):
        self.name = name

class Type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, name):
        self.name = name

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable=False)

    def __init__(self, name):
        self.name = name

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    temperature = db.Column(db.Float)
    brewtime = db.Column(db.Integer)
    boiled = db.Column(db.Boolean)

    def __init__(self, user, content, temperature, brewtime, boiled):
        self.user = user
        self.content = content
        self.temperature = temperature
        self.brewtime = brewtime
        self.boiled = boiled

class TeaIngredient(db.Model):
    tea = db.Column(db.Integer, db.ForeignKey('tea.id')
    ingredient = db.Column(db.Integer, db.ForeignKey('ingredient.id')

    def __init__(self, tea, ingredient):
        self.tea = tea
        self.ingredient = ingredient
