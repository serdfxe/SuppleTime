from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from SuppleTime.pr.app.models.turbo import turbo

from datetime import datetime



socket = Blueprint("turbo", __name__)


@socket.route("/main", methods=["GET"])
def main_route():
    return render_template("socket/main.html")


@socket.route("/form", methods=["GET"])
def form_routre():
    now = datetime.now().strftime("%H:%M:%S")
    with current_app.app_context():
        turbo.push(turbo.replace(render_template('socket/inner.html', now=now), "time"))
    return now