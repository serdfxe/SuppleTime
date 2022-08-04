from flask import Blueprint, render_template, request, redirect, url_for
from random import randint


root = Blueprint("root", __name__)

# def get_list_colors(color):
#     return (color,  [i - 16 for i in color], [i - 26 for i in color])


@root.route("/", methods=['GET', 'POST'])
def chil_page_route():
    return redirect(url_for("main.empty_route"))
