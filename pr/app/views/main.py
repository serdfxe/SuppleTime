from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from functools import wraps

from datetime import datetime

from random import randint

from SuppleTime.pr.app.models.turbo import turbo

from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models.user.services import *



main = Blueprint("main", __name__)

container = Container()


def tracker_decorator(f):
    @wraps(f)
    def dec(*args, **kwargs):
        r = f(*args, **kwargs)

        turbo.replace(target="messages", content=render_template("main/flashes.html"), to=current_user.id)

        state = get_tracker_state(current_user.id)
        turbo.socket.emit("change_state", state, to=current_user.id)

        tasks = get_all_users_tasks_by_date(current_user.id, datetime.now())
        turbo.replace(target="daylist", content=render_template("main/tracker/list.html", tracked_tasks=tasks), to=current_user.id)
        return r
    return dec 


@main.route("/", methods=['GET', 'POST'])
@login_required
def empty_route():
    return redirect(url_for("main.profile_route"))


# @main.route("tracker/change_state", methods=["POST"])
# @login_required
# def change_state_route():
#     action = request.form.get("action")
#     if action:
#         pass

#     return ""


@main.route("tracker/post_task", methods=["POST"])
@login_required
@tracker_decorator
def post_task_route():
    tracked_user_id = current_user.id
    mes = post_task(request.form, tracked_user_id)
    flash(*mes)
    return ""


@main.route("tracker/post_tracked_task", methods=["POST"])
@login_required
@tracker_decorator
def post_tracked_task_route():
    tracked_user_id = current_user.id
    stop_tracker(tracked_user_id)
    return ""

 
@main.route("tracker/pause", methods=["POST"])
@login_required
@tracker_decorator
def pause_route():
    pause_tracker(current_user.id)
    return ""


@turbo.socket.on("start")
@login_required
@tracker_decorator
def start_r(data):
    name = data["name"]
    start_tracker(current_user.id, name if name else "")
    return ""


@turbo.socket.on("billable")
@login_required
@tracker_decorator
def change_billable_route():
    change_billable(current_user.id)
    return ""


@turbo.socket.on("state")
@login_required
def state_geter():
    state = get_tracker_state(current_user.id)
    turbo.socket.emit("change_state", state, to=current_user.id)
    return state


@turbo.socket.on("change_day")
@login_required
def change_day_r(data):
    d = datetime.strptime(data["date"],"%Y-%m-%d")
    tasks = get_all_users_tasks_by_date(current_user.id, d)
    turbo.replace(target="daylist", content=render_template("main/tracker/list.html", tracked_tasks=tasks, current_date=data["date"]), to=current_user.id)
    


@main.route("tracker/start", methods=["POST"])
@login_required
@tracker_decorator
def start_route():
    data = request.form
    name = data.get("name")
    billable = data.get("billable")
    start_tracker(current_user.id, name, True if billable else False)
    return ""


@main.route("tracker/delete_task", methods=["POST"])
@login_required
@tracker_decorator
def delete_task_route():
    turbo.socket.emit("mess", str(request.form))
    mes = delete_task(request.form.get("task_id"))
    flash(*mes)
    return ""


@main.route("/tracker", methods=["GET"])    
@login_required
def tracker_route():
    tasks = get_all_users_tasks_by_date(current_user.id, datetime.now())
    state = get_tracker_state(current_user.id)
    return render_template("main/tracker/tracker.html", tracked_tasks=tasks, sidebar_components=sidebar_components, current="tracker", url_for_sidebar_components=url_for_sidebar_components, content=content["account"], name=current_user.name, state=state)


@main.post("/create_tag")
@login_required
@tracker_decorator
def create_tag_route():
    data = request.form
    ws_id = data.get("workspace_id")
    name = data.get("name")
    if not name: name = ''

    user_id = current_user.id

    if ws_id:
        if is_user_in_ws(user_id, workspace_id):
            success = create_tag(ws_id, name)
        else:
            flash("Undefind Error", "error")
    else:
        success = create_tag(get_users_default_ws(user_id).id, name)

    if success:
        flash("Success", "success")
    else:
        flash("Error", "error")

    flash(str(request.form), "message")

    return ""


@turbo.socket.on("tag_search")
def tag_search_handler(data):
    s = data["request"]
    turbo.socket.emit("tag_search", get_all_users_tags(current_user.id))


@main.post("/tracker/add_tracker_tag")
@login_required
@tracker_decorator
def add_tracker_tag_route():
    data = request.form
    tag_id = data.get("tag_id")
    user_id = current_user.id

    mess = add_tag_to_tracker(user_id, tag_id)

    if not mess: flash("Error", "error")

    return ""

@main.route("/account", methods=("GET", "POST"))
@login_required
def profile_route():
    return render_template("main/account.html", sidebar_components=sidebar_components, current="account", url_for_sidebar_components=url_for_sidebar_components, content=content["account"], name=current_user.name)


@main.route("/<s>", methods=['GET', 'POST'])
@login_required
def root_page_route(s):
    return render_template("main/main.html", sidebar_components=sidebar_components, current=s, url_for_sidebar_components=url_for_sidebar_components, content=content[s], name=current_user.name)
