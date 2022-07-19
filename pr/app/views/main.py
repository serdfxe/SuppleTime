from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from SuppleTime.pr.app.models.turbo import turbo

from datetime import datetime

from random import randint

from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models.user.services import *



main = Blueprint("main", __name__)

container = Container()


# @turbo.user_id
# def get_user_id():
#     return current_user.id


@main.route("/", methods=['GET', 'POST'])
@login_required
def empty_route():
    return redirect(url_for("main.profile_route", s='main'))


@main.route("tracker/change_state", methods=["POST"])
def change_state_route():
    action = request.form.get("action")
    if action:
        pass

    return ""


@main.route("tracker/post_task", methods=["POST"])
def post_task_route():
    tracked_user_id = current_user.id
    mes = post_task(request.form, tracked_user_id)
    flash(*mes)
    return redirect(url_for("main.tracker_route"))


@main.route("tracker/post_tracked_task", methods=["POST"])
def post_tracked_task_route():
    tracked_user_id = current_user.id
    stop_tracker(tracked_user_id)
    return redirect(url_for("main.tracker_route"))

 
@main.route("tracker/pause", methods=["POST"])
def pause_route():
    pause_tracker(current_user.id)
    return redirect(url_for("main.tracker_route"))


@main.route("tracker/start", methods=["POST"])
def start_route():
    data = request.form
    name = data.get("name")
    billable = data.get("billable")
    start_tracker(current_user.id, name, True if billable else False)
    return redirect(url_for("main.tracker_route"))


@main.route("tracker/delete_task", methods=["POST"])
def delete_task_route():
    mes = delete_task(request.form.get("task_id"))
    flash(*mes)
    return redirect(url_for("main.tracker_route"))


@main.route("/tracker", methods=["GET"])    
@login_required
def tracker_route():
    tasks = get_all_users_tasks_by_date(current_user.id, datetime.now())
    state = get_tracker_state(current_user.id)
    return render_template("main/tracker/tracker.html", tracked_tasks=tasks, sidebar_components=sidebar_components, current="tracker", url_for_sidebar_components=url_for_sidebar_components, content=content["account"], name=current_user.name, state=state)


@main.route("/account", methods=("GET", "POST"))
@login_required
def profile_route():
    return render_template("main/account.html", sidebar_components=sidebar_components, current="account", url_for_sidebar_components=url_for_sidebar_components, content=content["account"], name=current_user.name)


# @main.route("/main", methods=["GET"])
# def turbo_route():
#     return render_template("main.html")


# @main.route("/form", methods=["POST"])
# def form_route():
#     with current_app.app_context():
#         turbo.push(turbo.replace(render_template('inner.html', now=datetime.now().strftime("%H:%M:%S")), "time"), to=current_user.id)
#     return ""


@main.route("/<s>", methods=['GET', 'POST'])
@login_required
def root_page_route(s):
    return render_template("main/main.html", sidebar_components=sidebar_components, current=s, url_for_sidebar_components=url_for_sidebar_components, content=content[s], name=current_user.name)
