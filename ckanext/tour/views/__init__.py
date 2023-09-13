from __future__ import annotations

from sys import prefix

from flask import Blueprint

from ckanext.admin_panel.utils import ap_before_request
from ckanext.tour.views.tour_add import TourAddStepView, TourAddView
from ckanext.tour.views.tour_config import TourConfigView
from ckanext.tour.views.tour_delete import TourDeleteView, TourStepDeleteView
from ckanext.tour.views.tour_list import TourListView
from ckanext.tour.views.tour_update import TourUpdateView

tour = Blueprint("tour", __name__, url_prefix="/admin_panel/config/tour")
tour.before_request(ap_before_request)


tour.add_url_rule("/", view_func=TourConfigView.as_view("config"))
tour.add_url_rule("/list", view_func=TourListView.as_view("list"))
tour.add_url_rule("/new", view_func=TourAddView.as_view("add"))
tour.add_url_rule("/delete/<tour_id>", view_func=TourDeleteView.as_view("delete"))
tour.add_url_rule("/delete_step/<tour_step_id>", view_func=TourStepDeleteView.as_view("delete_step"))
tour.add_url_rule("/edit/<tour_id>", view_func=TourUpdateView.as_view("edit"))
tour.add_url_rule("/add_step", view_func=TourAddStepView.as_view("add_step"))


def get_blueprints():
    return [tour]
