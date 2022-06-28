from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager

from SuppleTime.pr.app.models.user.services import *


auth = Blueprint("auth", __name__)
container = Container()


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
        #flash("EROR", "eror")
        mes = login(request.form)
        flash(mes[0],mes[1])
        return redirect(url_for("main.root_page_route", s='account'))
        #return render_template("signin.html")


@auth.route('/', methods=("GET", "POST"))
def auth_rout():
    return redirect(url_for("auth.signin_route"))
    

@auth.route("/confirmemail/<s>")
def confirm_email_route(s):
    user = get_nonconfirmed_user_by_token(s)

    if user:
        if create_user(user.email.split("@")[0], user.email, user.password_hash):
            return "Success"
        return "Little bit Not Success"
    return "Not Success"
        

    
#@auth.route('/check_password', methods=("GET", "POST"))
#def check_password_route():
#    if request.method == "GET"
      
