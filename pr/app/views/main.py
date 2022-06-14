from flask import Blueprint, render_template
from app.config import *
from app.containers import Container
from app.models import *

from app.models.services import get_all_users


main = Blueprint("main", __name__)
container = Container()

get_all_users()


@main.route("/", methods=['GET', 'POST'])
def root_page_route():
    return render_template('eror.html')


@main.route("/users", methods=('GET', 'POST'))
def get_all_users_route():
    return []


@main.route("/user/<id>", methods=('GET', 'POST'))
def get_user(id):
    return 'user'


@main.route("/create", methods=('GET', 'POST'))
def create_user_route():
    pass
