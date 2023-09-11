from __future__ import annotations

from datetime import datetime as dt
from typing import Any, cast

import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.logic import validate

import ckanext.tour.logic.schema as schema
import ckanext.tour.model as tour_model
from ckanext.tour.exception import TourStepFileError


@tk.side_effect_free
@validate(schema.tour_show)
def tour_show(context, data_dict):
    tk.check_access("tour_show", context, data_dict)

    return tour_model.Tour.get(data_dict["id"]).dictize(context)  # type: ignore


@tk.side_effect_free
@validate(schema.tour_list)
def tour_list(context, data_dict):
    """Return a list of tours from database"""
    tk.check_access("tour_list", context, data_dict)

    query = model.Session.query(tour_model.Tour)

    if data_dict.get("state"):
        query = query.filter(tour_model.Tour.state == data_dict["state"])

    query = query.order_by(tour_model.Tour.created_at.desc())

    return [tour.dictize(context) for tour in query.all()]


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
        step.delete()

    tour.delete()

    context["session"].commit()

    return True


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
                    "upload": image.get("upload"),
                    "url": image.get("url"),
                    "tour_step_id": tour_step.id,
                },
            )
        except TourStepFileError as e:
            raise tk.ValidationError(f"Error while uploading step image: {e}")

    return tour_step.dictize(context)


@validate(schema.tour_update)
def tour_update(context, data_dict):
    tk.check_access("tour_update", context, data_dict)

    tour = cast(tour_model.Tour, tour_model.Tour.get(data_dict["id"]))

    tour.title = data_dict["title"]
    tour.anchor = data_dict["anchor"]
    tour.page = data_dict["page"]

    model.Session.commit()

    steps: list[dict[str, Any]] = data_dict.pop("steps", [])

    # TODO: how to delete steps?... Probably, with JS, add ID to some field
    # form_steps: set[str] = {step["id"] for step in steps}
    # tour_steps: set[str] = {step.id for step in tour.steps}

    # for step_id in tour_steps - form_steps:
    #     tk.get_action("tour_step_remove")(
    #         {"ignore_auth": True},
    #         {"id": step_id},
    #     )

    for step in steps:
        if step.get("id"):
            tk.get_action("tour_step_update")(
                {"ignore_auth": True},
                step,
            )
        else:
            step["tour_id"] = tour.id

            tk.get_action("tour_step_create")(
                {"ignore_auth": True},
                step,
            )

    return tour.dictize(context)


@validate(schema.tour_step_update)
def tour_step_update(context, data_dict):
    tk.check_access("tour_step_update", context, data_dict)

    tour_step = cast(tour_model.TourStep, tour_model.TourStep.get(data_dict["id"]))

    tour_step.title = data_dict["title"]
    tour_step.element = data_dict["element"]
    tour_step.intro = data_dict["intro"]
    tour_step.position = data_dict["position"]

    if data_dict.get("image"):
        data_dict["image"][0]["tour_step_id"] = tour_step.id
        action = "tour_step_image_update" if tour_step.image else "tour_step_image_upload"

        try:
            tk.get_action(action)(
                {"ignore_auth": True}, data_dict["image"][0]
            )
        except TourStepFileError as e:
            raise tk.ValidationError(f"Error while uploading step image: {e}")

    model.Session.commit()

    return tour_step.dictize(context)


@validate(schema.tour_step_remove)
def tour_step_remove(context, data_dict):
    study_request = cast(tour_model.Tour, tour_model.TourStep.get(data_dict["id"]))

    study_request.delete()
    model.Session.commit()

    return True


@validate(schema.tour_step_image_schema)
def tour_step_image_upload(context, data_dict):
    tour_step_id = data_dict.pop("tour_step_id", None)

    if not any([data_dict.get("upload"), data_dict.get("url")]):
        raise TourStepFileError(tk._("You have to provide either file or URL"))

    if all([data_dict.get("upload"), data_dict.get("url")]):
        raise TourStepFileError(
            tk._("You cannot use a file and a URL at the same time")
        )

    if not data_dict.get("upload"):
        return tour_model.TourStepImage.create(
            {"url": data_dict["url"], "tour_step_id": tour_step_id}
        ).dictize(context)

    try:
        result = tk.get_action("files_file_create")(
            {"ignore_auth": True},
            {
                "name": f"Tour step image <{dt.utcnow().isoformat()}>",
                "upload": data_dict["upload"],
            },
        )
    except (tk.ValidationError, OSError) as e:
        raise TourStepFileError(str(e))

    data_dict["file_id"] = result["id"]

    return tour_model.TourStepImage.create(
        {"file_id": result["id"], "tour_step_id": tour_step_id}
    ).dictize(context)


@validate(schema.tour_step_image_update_schema)
def tour_step_image_update(context, data_dict):
    tk.check_access("tour_step_update", context, data_dict)

    if not any([data_dict.get("upload"), data_dict.get("url")]):
        raise TourStepFileError(tk._("You have to provide either file or URL"))

    if all([data_dict.get("upload"), data_dict.get("url")]):
        raise TourStepFileError(
            tk._("You cannot use a file and a URL at the same time")
        )

    tour_step_image = cast(
        tour_model.TourStepImage,
        tour_model.TourStepImage.get_by_step(data_dict["tour_step_id"]),
    )

    if not data_dict.get("upload"):
        tour_step_image.url = data_dict["url"]
        model.Session.commit()
        return tour_step_image.dictize(context)

    try:
        result = tk.get_action("files_file_create")(
            {"ignore_auth": True},
            {
                "id": tour_step_image.file_id,
                "upload": data_dict["upload"],
            },
        )
    except (tk.ValidationError, OSError) as e:
        raise TourStepFileError(str(e))

    tour_step_image.url = result["url"]

    model.Session.commit()

    return tour_step_image.dictize(context)
