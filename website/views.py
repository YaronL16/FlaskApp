from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note, Compliment
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

    # Check User is verified and that note is not empty
        if not current_user.verified:
            flash('Your account must be verified to start using my website. Check your email for the verification link.', category='error')
        
        elif len(note) < 1:
            flash('Note is empty', category='error')

        # If all is good, Create note
        else:
            new_note = Note(text=note, owner=current_user.id)
            db.session.add(new_note)
            db.session.commit()    
            flash('Note added', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.owner == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/profile')
@login_required
def profile():
    # Check if the user is logged in and verified
    if current_user.is_authenticated and current_user.verified:
        verification_status = "Verified"
    else:
        verification_status = "Not Verified"
    
    # Get basic user data
    username = current_user.username if current_user.is_authenticated else None
    email = current_user.email if current_user.is_authenticated else None

    return render_template('profile.html',
                           user=current_user,
                           verification_status=verification_status,
                           username=username,
                           email=email,)

@views.route('/tamar', methods=['GET', 'POST'])
@login_required
def tamar():
    if request.method == 'POST':
        compliment = request.form.get('compliment')

    # Check user is verify and compliment is not empty
        if not current_user.verified:
            flash('Your account must be verified to start using my website. Check your email for the verification link.', category='error')

        elif len(compliment) < 1:
            flash('Note is empty', category='error')

        # If all is good, Create Compliment
        else:
            new_compliment = Compliment(text=compliment)
            db.session.add(new_compliment)
            db.session.commit()    
            flash('Compliment added', category='success')
    
    # Get all compliments
    if current_user.is_authenticated:
        compliments = Compliment.query.all()

    return render_template('tamar.html',
                           user=current_user,
                           compliments=compliments)

@views.route('/delete-compliment', methods=['POST'])
@login_required
def delete_compliment():
    compliment = json.loads(request.data)
    complimentId = compliment['complimentId']
    compliment = Compliment.query.get(complimentId)
    if compliment:
        if current_user.username == "yaron":
            db.session.delete(compliment)
            db.session.commit()
        else:
            flash('Only Yaron can choose to delete Compliments.', category='error')

    return jsonify({})
