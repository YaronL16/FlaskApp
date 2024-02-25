from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .regex import check_regex
from .models import User
from . import emailer, db
import json
import jwt

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query db for matching user
        user = User.query.filter_by(username=username).first()

        # Confirm user is found
        if user:

            # Confirm password is correct
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully', category='success')
                return redirect(url_for('views.home'))
            
            # Wrong password
            else:
                flash('Incorrect password, try again', category='error')
        
        # User not found
        else:
            flash('This user does not exist', category='error')

    # Fore GET request
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Query database for current users with matching username or email
        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()
        
        # Perform input validity tests
        if user_by_username:
            flash('This Username is already in use, try a different one', category='error')
        elif user_by_email:
            flash('This E-mail is already in use', category='error')
        elif check_regex(email) == False:
            flash('Please use a vaild email address', category='error')
        elif len (username) < 3:
            flash('Please use a vaild username', category='error')
        elif password1 != password2:
            flash('Your passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Please use a vaild password', category='error')

        # If all is good, create the user
        else:
            new_user = User(email=email, username=username, verified=False, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            # Create a secure token that identifies the user
            token = jwt.encode({"email": email}, current_app.config["SECRET_KEY"], algorithm="HS256")

            # Send verification email
            emailer.send(
                subject="Verify e-mail for Yaron website",
                receivers=email,
                html_template="email/verify.html",
                body_params={
                    "token": token
                }
            )

            login_user(new_user, remember=True)
            flash('Your account has been created, check your e-mail inbox to verify your account.', category='success')
            return redirect(url_for('views.home'))
    
    # For GET or failed POST requests
    return render_template("register.html", user=current_user)


@auth.route("/verify-email/<token>")
def verify_email(token):
    # get email address imbedded in the URL
    data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    email = data["email"]

    # Verify user that matches the email address
    user = User.query.filter_by(email=email).first()
    user.verified = True
    db.session.commit()

    flash('Email verification successful!', 'success')
    return redirect(url_for('auth.login'))