from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from random import randint

from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models.user.services import *


main = Blueprint("main", __name__)
container = Container()


@main.route("/", methods=['GET', 'POST'])
def empty_route():
    return redirect(url_for("main.root_page_route", s='main'))


@login_required
@main.route("/account", methods=("GET", "POST"))
def profile_route():
    return render_template("main/account.html", sidebar_components=sidebar_components, current="account", url_for_sidebar_components=url_for_sidebar_components, content=content["account"], name=current_user.name)


@login_required
@main.route("/<s>", methods=['GET', 'POST'])
def root_page_route(s):
    return render_template("main.html", sidebar_components=sidebar_components, current=s, url_for_sidebar_components=url_for_sidebar_components, content=content[s], name=current_user.name)
