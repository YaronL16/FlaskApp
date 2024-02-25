from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define notes schema
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

# Define user schema
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    verified = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note')
