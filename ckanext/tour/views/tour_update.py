from __future__ import annotations

import ckan.plugins.toolkit as tk
import ckan.types as types
from flask import Blueprint
from flask.views import MethodView

from ckanext.admin_panel.utils import ap_before_request

tour = Blueprint("tour", __name__)
tour.before_request(ap_before_request)


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
