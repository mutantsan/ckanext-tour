from __future__ import annotations

from typing import Any, cast
from datetime import datetime as dt

import ckan.plugins.toolkit as tk
from ckan.logic import validate

import ckanext.tour.logic.schema as schema
import ckanext.tour.model as tour_model
from ckanext.tour.exception import TourStepFileError


@tk.side_effect_free
@validate(schema.tour_list)
def tour_list(context, data_dict):
    tk.check_access("tour_list", context, data_dict)

    tours = tour_model.Tour.all()

    return [tour.dictize(context) for tour in tours]


@validate(schema.tour_create)
def tour_create(context, data_dict):
    tk.check_access("tour_create", context, data_dict)

    steps: list[dict[str, Any]] = data_dict.pop("steps", [])
    tour = tour_model.Tour.create(data_dict)

    for step in steps:
        step["tour_id"] = tour.id

        tk.get_action("tour_step_create")(
            {"ignore_auth": True},
            step,
        )

    return tour.dictize(context)


@validate(schema.tour_remove)
def tour_remove(context, data_dict):
    tk.check_access("tour_remove", context, data_dict)

    tour = cast(tour_model.Tour, tour_model.Tour.get(data_dict["id"]))

    for step in tour.steps:
        step.remove()

    tour = tour_model.Tour.create(data_dict)

    return tour.dictize(context)


@validate(schema.tour_step_schema)
def tour_step_create(context, data_dict):
    tk.check_access("tour_create", context, data_dict)

    images = data_dict.pop("image", [])

    if len(images) > 1:
        raise tk.ValidationError({"image": "only 1 image for step allowed"})

    tour_step = tour_model.TourStep.create(data_dict)

    for image in images:
        try:
            tk.get_action("tour_step_image_upload")(
                {"ignore_auth": True},
                {
                    "name": f"Tour step image <{dt.utcnow().isoformat()}>",
                    "upload": image.get("upload"),
                    "url": image.get("url"),
                    "tour_step_id": tour_step.id,
                },
            )
        except TourStepFileError as e:
            raise tk.ValidationError(f"Error while uploading step image: {e}")

    return tour_step.dictize(context)


@validate(schema.tour_step_image_schema)
def tour_step_image_upload(context, data_dict):
    tour_step_id = data_dict.pop("tour_step_id", None)

    try:
        result = tk.get_action("files_file_create")(
            {"ignore_auth": True},
            {"name": data_dict["name"], "upload": data_dict["upload"]},
        )
    except (tk.ValidationError, OSError) as e:
        raise TourStepFileError(str(e))

    data_dict["file_id"] = result["id"]

    return tour_model.TourStepImage.create(
        {"file_id": result["id"], "tour_step_id": tour_step_id}
    ).dictize(context)
