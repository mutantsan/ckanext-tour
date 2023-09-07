from __future__ import annotations

from typing import Any, Dict

from ckan.logic.schema import validator_args

from ckanext.tour.model import Tour, TourStep

Schema = Dict[str, Any]


@validator_args
def tour_show(not_empty, unicode_safe, tour_tour_exist) -> Schema:
    return {"id": [not_empty, unicode_safe, tour_tour_exist]}


@validator_args
def tour_create(
    not_empty, ignore, ignore_missing, unicode_safe, user_id_or_name_exists
) -> Schema:
    step_schema = tour_step_schema()
    step_schema["tour_id"] = [ignore_missing]

    return {
        "title": [not_empty, unicode_safe],
        "anchor": [ignore_missing, unicode_safe],
        "page": [ignore_missing, unicode_safe],
        "author_id": [not_empty, user_id_or_name_exists],
        "steps": step_schema,
        "__extras": [ignore],
    }


@validator_args
def tour_update(
    not_empty,
    unicode_safe,
    tour_tour_exist,
) -> Schema:
    tour_schema = tour_create()
    tour_schema["id"] = [not_empty, unicode_safe, tour_tour_exist]
    tour_schema["steps"] = tour_step_update()
    return tour_schema


@validator_args
def tour_step_schema(
    not_empty, ignore, ignore_missing, unicode_safe, default, one_of, tour_tour_exist
) -> Schema:
    image_schema = tour_step_image_schema()
    image_schema["tour_step_id"] = [ignore_missing]
    image_schema["name"] = [ignore_missing]

    return {
        "title": [ignore_missing, unicode_safe],
        "element": [not_empty, unicode_safe],
        "intro": [ignore_missing, unicode_safe],
        "position": [
            default(TourStep.Position.bottom),
            one_of(
                [
                    TourStep.Position.bottom,
                    TourStep.Position.top,
                    TourStep.Position.left,
                    TourStep.Position.right,
                ]
            ),
        ],
        "url": [ignore_missing, unicode_safe],
        "image": image_schema,
        "tour_id": [not_empty, unicode_safe, tour_tour_exist],
        "__extras": [ignore],
    }


@validator_args
def tour_step_update(
    not_empty,
    unicode_safe,
    tour_tour_step_exist,
) -> Schema:
    step_schema = tour_step_schema()
    step_schema.pop("tour_id")
    step_schema["id"] = [not_empty, unicode_safe, tour_tour_step_exist]

    return step_schema


@validator_args
def tour_step_image_schema(not_missing, unicode_safe, tour_tour_step_exist) -> Schema:
    return {
        "name": [not_missing, unicode_safe],
        "upload": [not_missing],
        "tour_step_id": [not_missing, unicode_safe, tour_tour_step_exist],
    }


@validator_args
def tour_list(ignore_empty, one_of) -> Schema:
    return {
        "state": [ignore_empty, one_of([Tour.State.active, Tour.State.inactive])],
    }


@validator_args
def tour_remove(not_empty, unicode_safe, tour_tour_exist) -> Schema:
    return {"id": [not_empty, unicode_safe, tour_tour_exist]}


@validator_args
def tour_step_remove(not_empty, unicode_safe, tour_tour_step_exist) -> Schema:
    return {"id": [not_empty, unicode_safe, tour_tour_step_exist]}
