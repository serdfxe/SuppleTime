from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from SuppleTime.pr.app.models.turbo import turbo



socket = Blueprint("socket", __name__)


@socket.route("/main", methods=["GET"])
def d():
    return render_template("socket/sock.html")


@socket.route("/send_form", methods=["GET"])
def send_form_route():
    return "<form action='/sock/send' method='post'><input type='text' name='var'><input type='submit'></form>"


@socket.route("/send", methods=["POST"])
def send_route():
    turbo.emit("mess", request.form)
    return redirect(url_for("socket.send_form_route"))


@turbo.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    print(request.namespace)


@turbo.on('connect')
def con():
    turbo.emit("mess", "hi!")