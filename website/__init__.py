from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ogni tua piccola lacrima e oceano sopra il mio viso'

    return app
