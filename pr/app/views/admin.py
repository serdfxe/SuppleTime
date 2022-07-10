from flask import Blueprint, render_template, request

from SuppleTime.pr.app.config import *

from SuppleTime.pr.app.containers import Container

from SuppleTime.pr.app.models.user.services import *
from SuppleTime.pr.app.models.Workspace.services import *


admin = Blueprint("admin", __name__)
container = Container()


def create_form(action: str, tasks):
    form = f"<form action='{action}' method='post'>"
    for i in tasks:
        form += f"<input type='{i[0]}' name='{i[1]}' value='{i[-1]}'>"
    return form+"<input type='submit'></form>"


@admin.route("/users", methods=('GET', 'POST'))
def get_all_users_route():
    return str([(i.email, i.name, i.id, i.confirm_users.password_hash) for i in get_all_users()])


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


@admin.route("/task_form", methods=["GET"])
def track_route():
    return create_form("/admin/post_task", [["text", "name"], ["time", "date_one"], ["time", "date_two"], ["checkbox", "billable"]])


@admin.route("/post_task", methods=["POST"])
def create_task_route():
    return str(request.form)