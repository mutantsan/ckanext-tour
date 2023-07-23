from __future__ import annotations
from attr import field

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk


tour = Blueprint("tour", __name__)


class TourListView(MethodView):
    def get(self) -> str:
        return tk.render("tour/tour_list.html")


class TourAddView(MethodView):
    def get(self) -> str:
        return tk.render("tour/tour_add.html", extra_vars={"data": {}})

    def post(self) -> str:
        data_dict = self._parse_data_dict()

        return tk.render(
            "tour/tour_add.html", extra_vars={"data": data_dict, "errors": {}}
        )

    def _parse_data_dict(self):
        step_fields = (
            "step_title",
            "step_element",
            "step_intro",
            "step_position",
            "image_url",
            "image_upload",
            "clear_upload"
        )

        steps = {}

        for field_name in step_fields:
            for idx, value in enumerate(tk.request.form.getlist(field_name)):
                steps.setdefault(idx, {})
                steps[idx][field_name] = value

        return {
            "title": tk.request.form.get("title"),
            "anchor": tk.request.form.get("anchor"),
            "page": tk.request.form.get("page"),
            "steps": [step for step in steps.values()],
        }


class TourAddStepView(MethodView):
    def post(self) -> str:
        step_idx = tk.asint(tk.request.form.get("stepId", 0))
        return tk.render("tour/tour_step.html", extra_vars={"step": {}})


class TourConfigView(MethodView):
    def get(self) -> str:
        return tk.render("tour/tour_list.html")

    def post(self) -> str:
        pass


tour.add_url_rule(
    "/admin_panel/config/tour", view_func=TourConfigView.as_view("config")
)
tour.add_url_rule(
    "/admin_panel/config/tour/list", view_func=TourListView.as_view("list")
)
tour.add_url_rule("/admin_panel/config/tour/new", view_func=TourAddView.as_view("add"))
tour.add_url_rule(
    "/admin_panel/config/tour/add_step", view_func=TourAddStepView.as_view("add_step")
)


def get_blueprints():
    return [tour]
