from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from SuppleTime.pr.app.models.turbo import turbo

import threading
from datetime import datetime
import time

socket = Blueprint("socket", __name__)


# @socket.route("/main", methods=["GET"])
# def d():
#     return render_template("socket/sock.html")


# @socket.route("/send_form", methods=["GET"])
# def send_form_route():
#     return "<form action='/sock/send' method='post'><input type='text' name='var'><input type='submit'></form>"


# @socket.route("/send", methods=["POST"])
# def send_route():
#     turbo.emit("mess", request.form)
#     return redirect(url_for("socket.send_form_route"))


# @turbo.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#     print(request.namespace)


# @turbo.on('connect')
# def con():
#     turbo.emit("mess", "hi!")


@turbo.user_id
def get_user_id():
    return current_user.id


@socket.route("/main/<s>", methods=["GET"])
def d(s):
    return render_template("socket/main.html", now=datetime.now().strftime("%H:%M:%S"))
    return render_template("sock.html")


# @turbo.socket.on("join")
# def conn(data):
#     room = data
#     join_room(room)
#     # send("Yes", to=room)
#     turbo.socket.emit("mess", f"You are in room {room}", room=room)


@socket.post("/form_data")
def f_r():
    return str(request.form)


@socket.route("/send_form", methods=["GET"])
def send_form_route():
    return "<form action='/send' method='post'><input type='text' name='var'><input type='text' name='room'><input type='submit'></form>"


@socket.route("/replace_form", methods=["GET"])
def replace_form_route():
    return "<form action='/replace' method='post'><input type='text' name='target'><input type='text' name='content'><input type='text' name='room'><input type='submit'></form>"


@socket.route("/replace", methods=["POST"])
def replace_route():
    turbo.replace(target=request.form.get("target"), content=request.form.get("content"), to="1")
    return redirect(url_for("replace_form_route"))


@socket.route("/send", methods=["POST"])
def send_route():
    turbo.socket.emit("mess", request.form, room=request.form.get("room"))
    # turbo.socket.emit("mess", str(clients))
    # turbo.socket.emit("mess", request.namespace)
    return redirect(url_for("send_form_route"))


@socket.get("/update")
def updfate_route():
    turbo.replace(render_template('socket/inner.html', now=datetime.now().strftime("%H:%M:%S")), "time", to=15)
    return "Yeeess"

# with current_app.app_context():
#     @current_app.context_processor
#     def inject_load():
#         with current_app.app_context():
#             return {"now": datetime.now().strftime("%H:%M:%S")}


# def update_load():
#     with app.app_context():
#         while True:
#             time.sleep(1)
#             turbo.replace(render_template('inner.html', now=datetime.now().strftime("%H:%M:%S")), "time", to="1")
#             # turbo.replace(render_template('inner.html', now=datetime.now().strftime("%H:%M:%S")), "time", to=0)


# threading.Thread(target=update_load).start()