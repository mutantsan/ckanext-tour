from flask import Blueprint


tour = Blueprint(
    "tour", __name__)


def page():
    return "Hello, tour!"


tour.add_url_rule(
    "/tour/page", view_func=page)


def get_blueprints():
    return [tour]
