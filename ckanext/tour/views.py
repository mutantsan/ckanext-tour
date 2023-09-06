from __future__ import annotations

from typing import Any

from flask import Blueprint
from flask.views import MethodView

import ckan.types as types
import ckan.plugins.toolkit as tk
from ckan.lib.helpers import Page

from ckanext.admin_panel.utils import ap_before_request

tour = Blueprint("tour", __name__)
tour.before_request(ap_before_request)


class TourListView(MethodView):
    def get(self) -> str:
        context: types.Context = {
            "user": tk.current_user.name,
            "auth_user_obj": tk.current_user,
        }

        return tk.render(
            "tour/tour_list.html",
            extra_vars={
                "page": self._get_pager(tk.get_action("tour_list")(context, {})),
                "columns": self._get_table_columns(),
                "bulk_options": self._get_bulk_actions(),
            },
        )

    def _get_pager(self, tour_list: list[dict[str, Any]]) -> Page:
        return Page(
            collection=tour_list,
            page=tk.h.get_page_number(tk.request.args),
            url=tk.h.pager_url,
            item_count=len(tour_list),
            items_per_page=10,
        )

    def _get_table_columns(self) -> list[dict[str, Any]]:
        return [
            tk.h.ap_table_column("title", "Title", sortable=False),
            tk.h.ap_table_column("anchor", "Anchor", sortable=False),
            tk.h.ap_table_column("page", "Page", sortable=False),
            tk.h.ap_table_column("state", "State", sortable=False),
            tk.h.ap_table_column(
                "steps", "Steps", column_renderer="tour_steps", sortable=False
            ),
            tk.h.ap_table_column(
                "actions",
                sortable=False,
                column_renderer="ap_action_render",
                width="10%",
                actions=[
                    tk.h.ap_table_action(
                        "tour.edit",
                        tk._("Delete"),
                        {"tour_id": "$id"},
                        attributes={"class": "btn btn-danger"},
                    ),
                    tk.h.ap_table_action(
                        "tour.edit",
                        tk._("Edit"),
                        {"tour_id": "$id"},
                    ),
                ],
            ),
        ]

    def _get_bulk_actions(self):
        return [
            {
                "value": "1",
                "text": tk._("Disable selected tour(s)"),
            },
            {
                "value": "2",
                "text": tk._("Enable selected tour(s)"),
            },
            {
                "value": "3",
                "text": tk._("Remove selected tour(s)"),
            },
        ]

    def post(self):
        tk.h.flash_success("Done!")

        context: types.Context = {
            "user": tk.current_user.name,
            "auth_user_obj": tk.current_user,
        }

        return tk.render(
            "tour/tour_list.html",
            extra_vars={
                "page": self._get_pager(tk.get_action("tour_list")(context, {})),
                "bulk_options": self._get_bulk_actions(),
            },
        )


class TourAddView(MethodView):
    def get(self) -> str:
        return tk.render("tour/tour_add.html", extra_vars={"data": {}})

    def post(self) -> str:
        data_dict = self._prepare_payload()

        try:
            tk.get_action("tour_create")(
                {
                    "user": tk.current_user.name,
                    "auth_user_obj": tk.current_user,
                },
                data_dict,
            )
        except tk.ValidationError as e:
            return tk.render(
                "tour/tour_add.html",
                extra_vars={
                    "data": data_dict,
                    "errors": e.error_dict,
                    "error_summary": e.error_summary,
                },
            )

        tk.h.flash_success(tk._("The tour has been created!"))

        return tk.render("tour/tour_add.html", extra_vars={"data": {}, "errors": {}})

    def _prepare_payload(self):
        step_fields = (
            "step_title",
            "step_element",
            "step_intro",
            "step_position",
            # "image_url",
            # "image_upload",
            # "clear_upload",
        )

        steps = {}

        for field_name in step_fields:
            _, field = field_name.split("_")

            for idx, value in enumerate(tk.request.form.getlist(field_name), start=1):
                # if field in ("url", "upload"):
                #     steps[idx].setdefault("image", [{}])
                #     steps[idx]["image"][0].update({field: value or None})
                # else:
                steps.setdefault(idx, {})
                steps[idx][field] = value

        for idx, file in enumerate(tk.request.files.getlist("step_upload"), start=1):
            if not file:
                continue

            steps[idx].setdefault("image", [{}])
            steps[idx]["image"][0].update({"upload": file or None})

        return {
            "title": tk.request.form.get("title"),
            "anchor": tk.request.form.get("anchor"),
            "page": tk.request.form.get("page"),
            "author_id": tk.current_user.id,  # type: ignore
            "steps": [step for step in steps.values()],
        }


class TourUpdateView(MethodView):
    def get(self, tour_id: str) -> str:
        context: types.Context = {
            "user": tk.current_user.name,
            "auth_user_obj": tk.current_user,
        }

        try:
            tour = tk.get_action("tour_show")(context, {"id": tour_id})
        except tk.ValidationError:
            return tk.render("tour/tour_404.html")

        return tk.render("tour/tour_edit.html", extra_vars={"tour": tour})

    def post(self) -> str:
        data_dict = {}

        try:
            tk.get_action("tour_update")(
                {
                    "user": tk.current_user.name,
                    "auth_user_obj": tk.current_user,
                },
                data_dict,
            )
        except tk.ValidationError as e:
            return tk.render(
                "tour/tour_edit.html",
                extra_vars={
                    "data": data_dict,
                    "errors": e.error_dict,
                    "error_summary": e.error_summary,
                },
            )

        tk.h.flash_success(tk._("The tour has been updated!"))

        return tk.render("tour/tour_add.html", extra_vars={"data": {}, "errors": {}})


class TourAddStepView(MethodView):
    def post(self) -> str:
        tk.asint(tk.request.form.get("stepId", 0))
        return tk.render("tour/snippets/tour_step.html", extra_vars={"step": {}})


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
    "/admin_panel/config/tour/edit/<tour_id>",
    view_func=TourUpdateView.as_view("edit"),
)
tour.add_url_rule(
    "/admin_panel/config/tour/add_step", view_func=TourAddStepView.as_view("add_step")
)


def get_blueprints():
    return [tour]
