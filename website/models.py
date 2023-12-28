from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    fullName = db.Column(db.String(250))
    total = db.Column(db.Integer)
    hours = db.relationship('Hours')
    
