from flask import Blueprint, render_template, request
from random import randint

from SuppleTime.pr.app.config import *
from SuppleTime.pr.app.containers import Container
from SuppleTime.pr.app.models.user.services import *


main = Blueprint("main", __name__)
container = Container()

color_list = [[16, 23, 39], [41, 52, 78], [88, 89, 107], [143, 143, 144], [197, 197, 197], [68, 79, 234], [93, 101, 214], [119, 128, 255], [159, 166, 255], [208, 211, 255], [26, 73, 127], [61, 109, 164], [105, 149, 200], [115, 171, 235], [80, 161, 255], [25, 86, 94], [77, 134, 141], [135, 177, 183], [124, 199, 209], [107, 227, 243], [23, 99, 62], [39, 142, 91], [54, 184, 121], [104, 220, 164], [148, 253, 202], [181, 158, 15], [246, 214, 9], [255, 235, 107], [255, 241, 152], [255, 250, 217], [206, 64, 71], [242, 56, 66], [255, 74, 83], [254, 111, 80], [253, 149, 76], [255, 55, 159], [255, 105, 183], [255, 148, 204], [255, 186, 222], [255, 217, 237]]


def get_list_colors(color):
    return (color,  [i - 16 for i in color], [i - 26 for i in color])


@main.route("/", methods=['GET', 'POST'])
def chil_page_route():
    color = color_list[randint(0, len(color_list) - 1)]
    return render_template("chil.html", color=get_list_colors(color))


@main.route("/<s>", methods=['GET', 'POST'])
def root_page_route(s):
    return render_template("main.html", sidebar_components=sidebar_components, current=s, url_for_sidebar_components=url_for_sidebar_components, content=content[s])
