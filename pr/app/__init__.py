from flask import Flask
from SuppleTime.pr.app.views.main import main
from SuppleTime.pr.app.views.admin import admin
from SuppleTime.pr.app.views.auth import auth

def create_app():
    app = Flask(__name__)
    app.debug = 0
    app.secret_key = b'sheeeeeeeeeesh'

    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')

    return app