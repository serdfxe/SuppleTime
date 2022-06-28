from flask import Flask

from SuppleTime.pr.app.views.main import main
from SuppleTime.pr.app.views.admin import admin
from SuppleTime.pr.app.views.auth import auth
from SuppleTime.pr.app.views.root import root

from SuppleTime.pr.app.models.user.login_manager import login_manager

#from SuppleTime.pr.app.containers import Container
#from dependency_injector.wiring import inject, Provide
#from SuppleTime.pr.app.database.repository import Repository
#from SuppleTime.pr.app.models.user.repository import UserRepository
#from SuppleTime.pr.app.models.user import User
#from SuppleTime.pr.app.database.session import Session

#from SuppleTime.pr.app.models.user.services import load_user

#userrep = UserRepository(Session)
#container = Container()


def create_app():
    app = Flask(__name__)
    app.debug = 0
    app.secret_key = b'sheeeeeeeeeesh'
    
    login_manager.init_app(app)

    app.register_blueprint(root)
    app.register_blueprint(main, url_prefix='/app')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    

    return app