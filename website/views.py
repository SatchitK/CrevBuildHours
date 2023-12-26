from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Hours
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        hour = request.form.get('hours')
        new_hour = Hours(data=hour, user_id=current_user.id) 
        db.session.add(new_hour) 
        db.session.commit()
        flash('Hours added!', category='success')

    return render_template("home.html", user=current_user)

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