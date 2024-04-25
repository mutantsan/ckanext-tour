from __future__ import annotations

from datetime import datetime as dt
from typing import Any, cast

import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.logic import validate

import ckanext.tour.logic.schema as schema
from ckanext.tour.model import Tour, TourStep, TourStepImage


@tk.side_effect_free
@validate(schema.tour_show)
def tour_show(context, data_dict):
    tk.check_access("tour_show", context, data_dict)

    return Tour.get(data_dict["id"]).dictize(context)  # type: ignore


@tk.side_effect_free
@validate(schema.tour_list)
def tour_list(context, data_dict):
    """Return a list of tours from database"""
    tk.check_access("tour_list", context, data_dict)

    query = model.Session.query(Tour)

    if data_dict.get("state"):
        query = query.filter(Tour.state == data_dict["state"])

    query = query.order_by(Tour.created_at.desc())

    return [tour.dictize(context) for tour in query.all()]


@validate(schema.tour_create)
def tour_create(context, data_dict):
    tk.check_access("tour_create", context, data_dict)

    steps: list[dict[str, Any]] = data_dict.pop("steps", [])
    tour = Tour.create(data_dict)

    for step in steps:
        step["tour_id"] = tour.id

        try:
            tk.get_action("tour_step_create")(
                {"ignore_auth": True},
                step,
            )
        except tk.ValidationError as e:
            tk.get_action("tour_remove")(
                {"ignore_auth": True},
                {"id": tour.id},
            )

            raise tk.ValidationError(e.error_dict if e else {})

    return tour.dictize(context)


@validate(schema.tour_remove)
def tour_remove(context, data_dict):
    tk.check_access("tour_remove", context, data_dict)

    tour = cast(Tour, Tour.get(data_dict["id"]))

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

    tour = cast(Tour, Tour.get(data_dict["tour_id"]))
    data_dict["index"] = len(tour.steps) + 1
    tour_step = TourStep.create(data_dict)

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
        except tk.ValidationError as e:
            raise tk.ValidationError(
                {"image": [f"Error while uploading step image: {e}"]}
            )

    return tour_step.dictize(context)


@validate(schema.tour_update)
def tour_update(context, data_dict):
    tk.check_access("tour_update", context, data_dict)

    tour = cast(Tour, Tour.get(data_dict["id"]))

    tour.title = data_dict.get("title", tour.title)
    tour.anchor = data_dict.get("anchor", tour.anchor)
    tour.page = data_dict.get("page", tour.page)
    tour.state = data_dict.get("state", tour.page)

    model.Session.commit()

    steps: list[dict[str, Any]] = data_dict.pop("steps", [])

    for step in steps:
        action = "tour_step_update" if step.get("id") else "tour_step_create"
        step["tour_id"] = tour.id

        try:
            tk.get_action(action)({"ignore_auth": True}, step)
        except tk.ValidationError as e:
            raise tk.ValidationError(e.error_dict)
    return tour.dictize(context)


@validate(schema.tour_step_update)
def tour_step_update(context, data_dict):
    tk.check_access("tour_step_update", context, data_dict)

    tour_step = cast(TourStep, TourStep.get(data_dict["id"]))

    tour_step.index = int(data_dict.get("index")) or tour_step.index
    tour_step.title = data_dict["title"]
    tour_step.element = data_dict["element"]
    tour_step.intro = data_dict["intro"]
    tour_step.position = data_dict["position"]

    if data_dict["clear"] and tour_step.image:
        tk.get_action("tour_step_image_remove")(
            {"ignore_auth": True}, {"id": tour_step.image.id}
        )
    elif data_dict.get("image"):
        data_dict["image"][0]["tour_step_id"] = tour_step.id

        try:
            tk.get_action(
                "tour_step_image_update"
                if tour_step.image
                else "tour_step_image_upload"
            )({"ignore_auth": True}, data_dict["image"][0])
        except tk.ValidationError as e:
            raise tk.ValidationError(
                {"image": [f"Error while uploading step image: {e}"]}
            )

    # model.Session.commit()

    return tour_step.dictize(context)


@validate(schema.tour_step_remove)
def tour_step_remove(context, data_dict):
    tour_step = cast(TourStep, TourStep.get(data_dict["id"]))

    tour_step.delete()
    model.Session.commit()

    return True


@validate(schema.tour_step_image_schema)
def tour_step_image_upload(context, data_dict):
    tour_step_id = data_dict.pop("tour_step_id", None)

    if not any([data_dict.get("upload"), data_dict.get("url")]):
        raise tk.ValidationError(tk._("You have to provide either file or URL"))

    if not data_dict.get("upload"):
        return TourStepImage.create(
            {"url": data_dict["url"], "tour_step_id": tour_step_id}
        ).dictize(context)

    try:
        result = tk.get_action("files_file_create")(
            {"ignore_auth": True},
            {
                "name": f"Tour step image <{tour_step_id}>",
                "upload": data_dict["upload"],
            },
        )
    except OSError as e:
        raise tk.ValidationError(str(e))

    data_dict["file_id"] = result["id"]

    return TourStepImage.create(
        {"file_id": result["id"], "tour_step_id": tour_step_id}
    ).dictize(context)


@validate(schema.tour_step_image_update_schema)
def tour_step_image_update(context, data_dict):
    tk.check_access("tour_step_update", context, data_dict)

    if not any([data_dict.get("upload"), data_dict.get("url")]):
        raise tk.ValidationError(tk._("You have to provide either file or URL"))

    tour_step_image = cast(
        TourStepImage,
        TourStepImage.get_by_step(data_dict["tour_step_id"]),
    )

    if not data_dict.get("upload"):
        tour_step_image.url = data_dict["url"]
        model.Session.commit()
        return tour_step_image.dictize(context)

    try:
        result = tk.get_action("files_file_create")(
            {"ignore_auth": True},
            {
                "name": f"Tour step image <{data_dict['tour_step_id']}>",
                "upload": data_dict["upload"],
            },
        )
    except (tk.ValidationError, OSError) as e:
        raise tk.ValidationError(str(e))

    tour_step_image.url = result["url"]

    model.Session.commit()

    return tour_step_image.dictize(context)


@validate(schema.tour_step_image_remove_schema)
def tour_step_image_remove(context, data_dict):
    tour_step_image = cast(TourStepImage, TourStepImage.get(data_dict["id"]))

    tour_step_image.delete(with_file=bool(tour_step_image.file_id))
    model.Session.commit()

    return True
