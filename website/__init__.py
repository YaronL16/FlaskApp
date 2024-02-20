from flask import Flask

# Create Flask App
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ogni tua piccola lacrima e oceano sopra il mio viso'

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
