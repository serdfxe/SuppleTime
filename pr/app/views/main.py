from flask import Blueprint, render_template
from pr.app.config import *
from pr.app.models import *


main = Blueprint("main", __name__)


@main.route("/", methods=('GET', 'POST'))
def root_page():
    return render_template('eror.html')
