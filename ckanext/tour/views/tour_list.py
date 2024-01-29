from __future__ import annotations

from typing import Any, Callable
from functools import partial

from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.lib.helpers import Page
from ckan.logic import parse_params

from ckanext.collection.shared import get_collection
from ckanext.ap_main.utils import ap_before_request

from ckanext.tour.model import Tour

tour = Blueprint("tour", __name__)
tour.before_request(ap_before_request)


class TourListView(MethodView):
    def get(self) -> str:
        return tk.render(
            "tour/tour_list.html",
            extra_vars={
                "collection": get_collection(
                    "tour-list", parse_params(tk.request.args)
                )
            },
        )

    def post(self):
        tk.h.flash_success("Done!")

        bulk_action = tk.request.form.get("bulk-action")
        entity_ids = tk.request.form.getlist("entity_id")

        action_func = self._get_bulk_action(bulk_action) if bulk_action else None

        if not action_func:
            tk.h.flash_error(tk._("The bulk action is not implemented"))
            return tk.redirect_to("ap_cron.manage")

        for entity_id in entity_ids:
            try:
                action_func(entity_id)
            except tk.ValidationError as e:
                tk.h.flash_error(str(e))

        return tk.redirect_to("tour.list")

    def _get_bulk_action(self, value: str) -> Callable[[str], None] | None:
        return {
            "1": partial(self._update_tour_state, state=Tour.State.inactive),
            "2": partial(self._update_tour_state, state=Tour.State.active),
            "3": self._remove_tour,
        }.get(value)

    def _update_tour_state(self, tour_id: str, state: str) -> None:
        tk.get_action("tour_update")(
            {"ignore_auth": True},
            {
                "id": tour_id,
                "state": state,
            },
        )

    def _remove_tour(self, tour_id: str) -> None:
        tk.get_action("tour_remove")(
            {"ignore_auth": True},
            {
                "id": tour_id,
            },
        )
