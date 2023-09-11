from __future__ import annotations

from typing import Any
import string
from urllib.parse import urlparse

import ckan.plugins.toolkit as tk
import ckan.types as types

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


def tour_tour_step_image_exist(v: str, context) -> Any:
    """Ensures that the tour step image exists for a specific tour step"""

    result = tour_model.TourStepImage.get_by_step(v)

    if not result:
        raise tk.Invalid(f"The tour image for tour step {v} doesn't exists.")

    return v


def tour_url_validator(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
) -> Any:
    """Checks that the provided value (if it is present) is a valid URL"""

    url = data.get(key, None)
    if not url:
        return

    try:
        pieces = urlparse(url)
        if (
            all([pieces.scheme, pieces.netloc])
            and set(pieces.netloc) <= set(string.ascii_letters + string.digits + "-.:")
            and pieces.scheme in ["http", "https"]
        ):
            return
    except ValueError:
        # url is invalid
        pass

    errors[key].append(tk._("Please provide a valid URL"))
