from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST': 
        email = request.form.get('email')
        fullName = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(fullName) < 2:
            flash('Name must greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords did not match', category='error')
        elif len(password1) < 5:
            flash('Password length must be greater than 5 characters', category='error')
        else:
            #add to database
            flash('Account created!', category='success')

    return render_template("signup.html")