from __future__ import annotations

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk


tour = Blueprint("tour", __name__)


class TourListView(MethodView):
    def get(self) -> str:
        return tk.render("tour/tour_list.html")


class TourAddView(MethodView):
    def get(self) -> str:
        return tk.render("tour/tour_list.html")

    def post(self) -> str:
        pass

tour.add_url_rule("/admin_panel/config/tour/", view_func=TourListView.as_view("list"))
tour.add_url_rule("/admin_panel/config/tour/new", view_func=TourAddView.as_view("add"))


def get_blueprints():
    return [tour]
