from application import db

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

class Timestamped(db.Model):
    __abstract__ = True

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
