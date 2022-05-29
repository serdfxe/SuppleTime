from flask import Flask
from app.views.main import main

def create_app():
    app = Flask(__name__)
    app.debug = 0
    app.secret_key = b'sheeeeeeeeeesh'

    app.register_blueprint(main)

    return app