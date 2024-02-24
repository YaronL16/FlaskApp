from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .regex import check_regex
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", text="Tamar")

@auth.route('/logout')
def logout():
    return "<p>Logout<p>"

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Perform input validity tests
        if check_regex(email) == False:
            flash('Please use a vaild email address', category='error')
        elif len (username) < 3:
            flash('Please use a vaild username', category='error')
        elif password1 != password2:
            flash('Your passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Please use a vaild password', category='error')

        # Else create user
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created', category='success')

            return redirect(url_for('views.home'))


    return render_template("register.html")