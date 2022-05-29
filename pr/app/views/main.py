from flask import Blueprint, render_template
from app.config import *
from app.models import *


main = Blueprint("main", __name__)


@main.route("/", methods=('GET', 'POST'))
def root_page():
    return render_template('eror.html')
