from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_redmail import RedMail
from os import path

# Define Database
db = SQLAlchemy()
DB_NAME = "database.db"

# Define Emailer
emailer = RedMail()

# Create Flask App
def create_app():
    app = Flask(__name__)

    # Define encryption key
    app.config['SECRET_KEY'] = 'ogni tua piccola lacrima e oceano sopra il mio viso'

    # Define DB file location and link flask app to DB
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Set up database
    from .models import User, Note
    create_database(app)

    # Setup login manager and tell it how to get user objects
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Set up email for app
    app.config["EMAIL_HOST"] = "smtp.gmail.com"
    app.config["EMAIL_PORT"] = 587
    app.config["EMAIL_USERNAME"] = "flaskyaron@gmail.com"
    app.config["EMAIL_PASSWORD"] = "ustq nwai yzxy mnsr"
    emailer.init_app(app)

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print("Created Database")
    