from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# Define Database
db = SQLAlchemy()
DB_NAME = "database.db"

# Create Flask App
def create_app():
    app = Flask(__name__)

    # Define encryption key
    app.config['SECRET_KEY'] = 'ogni tua piccola lacrima e oceano sopra il mio viso'

    # Define database file location
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Define Flask app for the database
    db.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Set up database
    from .models import User, Note
    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print("Created Database")
    