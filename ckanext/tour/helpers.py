import uuid

from ckanext.tour.model import TourStep


def tour_get_position_options():
    return [
        {"value": step, "text": step}
        for step in (
            TourStep.Position.bottom,
            TourStep.Position.top,
            TourStep.Position.right,
            TourStep.Position.left,
        )
    ]

def tour_random_step_id() -> str:
    return str(uuid.uuid4())
