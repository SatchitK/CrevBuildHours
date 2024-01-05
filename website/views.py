from flask import Blueprint, render_template, request, flash, jsonify, send_file
import io
import base64
from datetime import datetime
from flask_login import login_required, current_user
from .models import User, Hours
from . import db
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import func
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
import pytz
import os
import csv


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        hour = request.form.get('hour')
        try:
            if float(hour) and (float(hour) > 0.0):
                    hour_num = float(hour)
                    if hour_num <= 16:
                        todays_date = datetime.now(pytz.timezone('US/Eastern')).date()
                        todays_entries = Hours.query.filter(
                                         Hours.user_id == current_user.id,
                                         func.date(Hours.date)==todays_date).first();
                        if not todays_entries:
                            new_hour = Hours(data=hour, user_id=current_user.id) 
                            db.session.add(new_hour) 
                            db.session.commit()
                            flash('Hours added!', category='success')
                        else:
                            flash('You already entered hours today! Only 1 entry per day.', category='error')
                    else:
                        flash('Max hours per day are 16!', category='error')  
            else:
                flash('Hours entered must exceed 0.', category='error')
        except ValueError:
            flash('Your entry was not a number, make sure it is a decimal or integer number.', category='error')

    return render_template("home.html", user=current_user)

@views.route('/insights')
def insights():
    #update total hours per person
    total_entries_per_user = []
    users = User.query.all()
    for user in users:
        total = 0
        total_entries_per_user.append(len(user.hours))
        for hour in user.hours:
            total += hour.data
            User.query.filter_by(email=user.email).first().total = total
    
    #get arrays populated for export
    data = []
    avg_per_week_data = []
    labels = []
    date_time = []
    for user in users:
        data.append(User.query.filter_by(email=user.email).first().total)
        labels.append(User.query.filter_by(email=user.email).first().fullName)
        avg_per_week_data.append(User.query.filter_by(email=user.email).first().total / 15)
    
    # for hour in user.hours:
    #     date_time.append(hour.date)

    #hours logged each datewise (locally stored)
    # dates_only = []
    # for date in date_time:
    #     date_str = str(date)
    #     dates_only.append(date_str.split(" ")[0])
    # print(dates_only)

    # dates_df = pd.DataFrame({"raw_dates":dates_only})
    # print(dates_df)
    # sns.histplot(data=dates_df["raw_dates"])
    # plt.savefig("date_logs.png")
 
    #export data to simple 2 column csv
    df = pd.DataFrame({"Full Name": labels, "Hours" : data})
    df.to_csv("./member_hours.csv", index=False)
    csv_file = "./member_hours.csv"

    

    return render_template("insights.html", user=current_user, data=data, 
                           labels=labels, avg_pw = avg_per_week_data
                           ,entries_per_user = total_entries_per_user)

@views.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        newName = request.form.get('newName')
        newEmail = request.form.get('newEmail')
        if len(newEmail) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(newName) < 3:
            flash('Name must greater than 3 characters', category='error')
        else: 
            current_user.fullName = newName
            current_user.email = newEmail
    return render_template("update.html", user=current_user)


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








