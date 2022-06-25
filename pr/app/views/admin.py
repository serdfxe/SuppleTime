from flask import Blueprint, render_template, request

from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models.user.services import *


admin = Blueprint("admin", __name__)
container = Container()


@admin.route("/users", methods=('GET', 'POST'))
def get_all_users_route():
    return str([i.email for i in get_all_users()])


@admin.route("/user/<id>", methods=('GET', 'POST'))
def get_user_route(id):
    user = get_user(id=int(id)) 
    return user.name if user is not None else "No such user"


@admin.route("/create_user", methods=('POST', 'GET'))
def create_user_route():
    if request.method == "POST":
        return register_user(request.form)
    
    if request.method == "GET":
        return """<p> Hello, try post smth </p> <form class="form-test" method="post">
                <p>Name:</p>
	            <input type="text" value="" name="name">
                <p>Email:</p>
                <input type="text" value="" name="email">
                <p>Пароль:</p>
                <input type="text" value="" name="password">
	            <input type="submit" value="Register">
                </form>"""


@admin.route("/del", methods=('POST', 'GET'))
def delete_all_users_route():
    delete_all_users()
    return "OK"
