from flask import Blueprint, render_template, request
from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models.user.services import *


main = Blueprint("main", __name__)
container = Container()

print(get_user(1))
#print(create_user("Tolya ga1y", "mail@nai1l.com"))


@main.route("/main/<s>", methods=['GET', 'POST'])
def root_page_route(s):
    return render_template("main.html", sidebar_components=sidebar_components, current=s, url_for_sidebar_components=url_for_sidebar_components, content=content[s])


@main.route("/users", methods=('GET', 'POST'))
def get_all_users_route():
    return str([i.name for i in get_all_users()])


@main.route("/user/<id>", methods=('GET', 'POST'))
def get_user_route(id):
    user = get_user(id=int(id)) 
    return user.name if user is not None else "No such user"


@main.route("/create_user", methods=('POST', 'GET'))
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


@main.route("/del", methods=('POST', 'GET'))
def delete_all_users_route():
    delete_all_users()
    return "OK"
