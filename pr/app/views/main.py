from flask import Blueprint, render_template
from pr.app.config import *
from pr.app.containers import Container
from pr.app.models import *

from pr.app.models.services import *


main = Blueprint("main", __name__)
container = Container()

#print(create_user("Tolya ga1y", "mail@nai1l.com"))

@main.route("/", methods=['GET', 'POST'])
def root_page_route():
    return render_template('eror.html')


@main.route("/users", methods=('GET', 'POST'))
def get_all_users_route():
    return []


@main.route("/user/<id>", methods=('GET', 'POST'))
def get_user(id):
    return get_user(id=int(id))


@main.route("/create", methods=('GET', 'POST'))
def create_user_route():
    pass
