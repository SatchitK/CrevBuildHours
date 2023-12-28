from flask import Blueprint, render_template, request, flash, jsonify, send_file
import io
import base64
from flask_login import login_required, current_user
from .models import User, Hours
from . import db
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
import os
import csv


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        hour = request.form.get('hour')
        if hour.isdigit():
                if int(hour) <= 12:
                    new_hour = Hours(data=hour, user_id=current_user.id) 
                    db.session.add(new_hour) 
                    db.session.commit()
                    flash('Hours added!', category='success')
                else:
                    flash('Too many hours in one entry!', category='error')  
        else:
            flash('Invalid Hours!', category='error')

    return render_template("home.html", user=current_user)

@views.route('/insights')
def insights():
    users = User.query.all()
    for user in users:
        total = 0
        for hour in user.hours:
            total += hour.data
            User.query.filter_by(email=user.email).first().total = total
    
    data = []
    labels = []
    for user in users:
        data.append(User.query.filter_by(email=user.email).first().total)
        labels.append(User.query.filter_by(email=user.email).first().fullName)
    
    return render_template("insights.html", user=current_user, data=data, labels=labels)


@views.route('/delete-hour', methods=['POST'])
def delete_hour():
    hour = json.loads(request.data)
    hourId = hour['hourId']
    hour = Hours.query.get(hourId)
    if hour:
        if hour.user_id == current_user.id:
            db.session.delete(hour)
            db.session.commit()

    return jsonify({})








