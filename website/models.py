from . import db
from flask_login import UserMixin
from datetime import date
from sqlalchemy.sql import func

class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)
    date = db.Column(db.DateTime(), default=func.now(), server_default=func.timezone('EST'), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    fullName = db.Column(db.String(250))
    total = db.Column(db.Float)
    hours = db.relationship('Hours')
    
