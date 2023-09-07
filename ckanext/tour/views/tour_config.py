from __future__ import annotations

import ckan.plugins.toolkit as tk
from flask.views import MethodView


class TourConfigView(MethodView):
    def get(self) -> str:
        return tk.render("tour/tour_list.html")

    def post(self) -> str:
        return tk.render("tour/tour_list.html")
