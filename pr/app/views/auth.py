from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, logout_user, login_required, current_user

from SuppleTime.pr.app.models.user.services import *

from SuppleTime.pr.app.config import *


auth = Blueprint("auth", __name__)
container = Container()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/signin?next=' + request.path)


@auth.route('/signup', methods=("GET", "POST"))
def signup_route():
    if request.method == "POST":
        mes = preregister_user(request.form)
        flash(mes[0],mes[1])
    return render_template("auth/form.html", form=authforms["signup"])


@auth.route('/signin', methods=("GET", "POST"))
def signin_route():
    if request.method == "POST":
        #flash("EROR", "eror")
        mes = login(request.form)
        if mes[0] == "Success":
            return redirect(url_for("main.root_page_route", s='account') or request.args.get('next'))
        flash(mes[0],mes[1])
    return render_template("auth/form.html", form=authforms["signin"])


@auth.route('/', methods=("GET", "POST"))
def auth_root():
    return redirect(url_for("auth.signin_route"))


@auth.route("/confirmemail/<s>", methods=("GET", "POST"))
def confirm_email_route(s):
    user = get_nonconfirmed_user(confirm_token=s)

    if user:
        user = final_register_user(user)
        if user:
            login_user(user)
            return redirect(url_for("main.empty_route"))
        return "Little bit Not Success"
    return "Not Success"


@auth.route("/enterbymail", methods=("GET", "POST"))
def enterbyemail_route():
    if request.method == "POST":
        email = request.form["email"]
        flash(*send_enter_mail(email))
    return render_template("auth/form.html", form=authforms["enterbymail"])


@auth.route("/enterbymail/<s>", methods=("GET", "POST"))
def enterbytoken_route(s):
    user = get_confirmed_user(token=s)

    if user:
        login_user(user.users)
        return redirect(url_for("main.empty_route"))


@auth.route("/forgotpassword", methods=("GET", "POST"))
def forgotpassword_route():
    if request.method == "POST":
        email = request.form["email"]
        flash(*send_passwd_mail(email))
    return render_template("auth/form.html", form=authforms["forgotpassword"])


@auth.route("/passwordchange/<s>", methods=("GET", "POST"))
def passwordchange_route(s):
    user = get_confirmed_user(token=s)
    if user:
        if request.method == "POST":
            passwd1 = request.form["password1"]
            passwd2 = request.form["password2"]
            flash(*change_password(user, passwd1, passwd2))
    return render_template("auth/form.html", form=authforms["passwordchange"]) 


@auth.route("/logout", methods=["POST"])
@login_required
def logout_route():
    logout_user()
    return redirect(url_for("auth.auth_root"))


@auth.route("/delete_my_account", methods=["POST"])
@login_required
def delete_my_account_route():
    delete_user(current_user.id)
    return redirect(url_for("auth.auth_root"))


#@auth.route('/check_password', methods=("GET", "POST"))
#def check_password_route():
#    if request.method == "GET"
