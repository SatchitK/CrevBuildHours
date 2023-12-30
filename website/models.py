from . import db
from flask_login import UserMixin
from datetime import datetime
import pytz
from sqlalchemy.sql import func

class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=lambda:datetime.now(pytz.timezone('America/New_York')), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    fullName = db.Column(db.String(250))
    total = db.Column(db.Float)
    hours = db.relationship('Hours')
    
