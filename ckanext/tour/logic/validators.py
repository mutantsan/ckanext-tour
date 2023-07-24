from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk

import ckanext.tour.model as tour_model


def tour_tour_exist(v: str, context) -> Any:
    """Ensures that the tour with a given id exists"""

    result = tour_model.Tour.get(v)

    if not result:
        raise tk.Invalid(f"The tour with an id {v} doesn't exist.")

    return v


def tour_tour_step_exist(v: str, context) -> Any:
    """Ensures that the tour step with a given id exists"""

    result = tour_model.TourStep.get(v)

    if not result:
        raise tk.Invalid(f"The tour with an id {v} doesn't exist.")

    return v
