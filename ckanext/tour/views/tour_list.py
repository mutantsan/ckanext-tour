from __future__ import annotations

from typing import Any, Callable
from functools import partial

import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.lib.helpers import Page
from flask import Blueprint
from flask.views import MethodView

from ckanext.ap_main.utils import ap_before_request
from ckanext.tour.model import Tour

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
                        "tour.delete",
                        label=tk._("Delete"),
                        params={"tour_id": "$id"},
                        attributes={"class": "btn btn-danger"},
                    ),
                    tk.h.ap_table_action(
                        "tour.edit",
                        label=tk._("Edit"),
                        params={"tour_id": "$id"},
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

        return tk.render(
            "tour/tour_list.html",
            extra_vars={
                "page": self._get_pager(tk.get_action("tour_list")(context, {})),
                "columns": self._get_table_columns(),
                "bulk_options": self._get_bulk_actions(),
            },
        )

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
