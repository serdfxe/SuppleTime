from flask import Blueprint, render_template, request, redirect, url_for


auth = Blueprint("auth", __name__)


@auth.route('/signup', methods=("GET", "POST"))
def signup_route():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        pass
        
        
@auth.route('/signin', methods=("GET", "POST"))
def signin_route():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        pass


@auth.route('/', methods=("GET", "POST"))
def auth_rout():
    return redirect(url_for("auth.signin_route"))

