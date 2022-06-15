from flask import Blueprint, render_template
from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models import *

from SuppleTime.pr.app.models.services import *


main = Blueprint("main", __name__)
container = Container()

print(get_user(1))
#print(create_user("Tolya ga1y", "mail@nai1l.com"))

@main.route("/", methods=['GET', 'POST'])
def root_page_route():
    return render_template('eror.html')


@main.route("/users", methods=('GET', 'POST'))
def get_all_users_route():
    return str([i.name for i in get_all_users()])


@main.route("/user/<id>", methods=('GET', 'POST'))
def get_user_route(id):
    print("yeeees")
    return get_user(id=int(id)).name


@main.route("/create", methods=('GET', 'POST'))
def create_user_route():
    pass
