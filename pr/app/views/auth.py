from flask import Blueprint, render_template, request, redirect, url_for, flash
from SuppleTime.pr.app.models.user.services import *

auth = Blueprint("auth", __name__)


@auth.route('/signup', methods=("GET", "POST"))
def signup_route():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        mes = register_user(request.form)
        flash(mes[0],mes[1])
        return render_template("signup.html")
        
        
@auth.route('/signin', methods=("GET", "POST"))
def signin_route():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        flash("EROR", "eror")
        return render_template("signin.html")


@auth.route('/', methods=("GET", "POST"))
def auth_rout():
    return redirect(url_for("auth.signin_route"))
