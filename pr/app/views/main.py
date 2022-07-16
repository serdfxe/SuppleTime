from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

# from SuppleTime.pr.app.models.turbo import turbo

from datetime import datetime

from random import randint

from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models.user.services import *


main = Blueprint("main", __name__)

container = Container()


# @turbo.user_id
# def get_user_id():
#     print(current_user.id)
#     return current_user.id


@main.route("/", methods=['GET', 'POST'])
@login_required
def empty_route():
    return redirect(url_for("main.profile_route", s='main'))


# @main.route("tracker/post_task", methods=["POST"])
# def post_task_route():
#     tracked_user_id = current_user.id
#     mes = post_task(request.form, tracked_user_id)
#     # with current_app.app_context():
#     tasks = [("123", True, "123123")]
#         #tasks = [(i.name, i.billable, get_differ_time(i.date_one, i.date_two)) for i in get_all_users_tasks_by_date(current_user.id, datetime.now())]
#     return turbo.stream(turbo.push(turbo.replace(render_template('main/tracker/tracker.html', tracked_tasks=tasks), "daylist"), to=current_user.id))

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


@main.route("tracker/delete_task", methods=["POST"])
def delete_task_route():
    mes = delete_task(request.form.get("task_id"))
    flash(*mes)
    return redirect(url_for("main.tracker_route"))


@main.route("/tracker", methods=["GET"])    
@login_required
def tracker_route():
    # flash("Ok", "message")
    # flash("Error sdg sdfsdf sd fsdf srgnosd oi sdofin w!", "error")
    # flash("Success", "success")
    tasks = [(i.name, i.billable, i.date_one.strftime("%H:%M"), i.date_two.strftime("%H:%M"), get_differ_time(i.date_one, i.date_two), i.id) for i in get_all_users_tasks_by_date(current_user.id, datetime.now())]
    return render_template("main/tracker/tracker.html", tracked_tasks=tasks, sidebar_components=sidebar_components, current="tracker", url_for_sidebar_components=url_for_sidebar_components, content=content["account"], name=current_user.name)


@main.route("/account", methods=("GET", "POST"))
@login_required
def profile_route():
    return render_template("main/account.html", sidebar_components=sidebar_components, current="account", url_for_sidebar_components=url_for_sidebar_components, content=content["account"], name=current_user.name)


@main.route("/<s>", methods=['GET', 'POST'])
@login_required
def root_page_route(s):
    return render_template("main/main.html", sidebar_components=sidebar_components, current=s, url_for_sidebar_components=url_for_sidebar_components, content=content[s], name=current_user.name)
