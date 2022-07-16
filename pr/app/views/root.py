from flask import Blueprint, render_template, request, redirect, url_for
from random import randint


root = Blueprint("root", __name__)

color_list = [[16, 23, 39], [41, 52, 78], [88, 89, 107], [143, 143, 144], [197, 197, 197], [68, 79, 234], [93, 101, 214], [119, 128, 255], [159, 166, 255], [208, 211, 255], [26, 73, 127], [61, 109, 164], [105, 149, 200], [115, 171, 235], [80, 161, 255], [25, 86, 94], [77, 134, 141], [135, 177, 183], [124, 199, 209], [107, 227, 243], [23, 99, 62], [39, 142, 91], [54, 184, 121], [104, 220, 164], [148, 253, 202], [181, 158, 15], [246, 214, 9], [255, 235, 107], [255, 241, 152], [255, 250, 217], [206, 64, 71], [242, 56, 66], [255, 74, 83], [254, 111, 80], [253, 149, 76], [255, 55, 159], [255, 105, 183], [255, 148, 204], [255, 186, 222], [255, 217, 237]]


def get_list_colors(color):
    return (color,  [i - 16 for i in color], [i - 26 for i in color])


@root.route("/", methods=['GET', 'POST'])
def chil_page_route():
    color = color_list[randint(0, len(color_list) - 1)]
    return redirect(url_for("main.empty_route"))
    return render_template("chil.html", color=get_list_colors(color))
