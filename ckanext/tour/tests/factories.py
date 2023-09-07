from io import BytesIO

import factory
from ckan.tests import factories

from ckanext.tour import model as tour_model
from ckanext.tour.tests.helpers import CSV_DATA, FakeFileStorage


class TourStepImageFactory(factories.CKANFactory):
    class Meta:
        model = tour_model.TourStepImage
        action = "tour_step_image_upload"

    tour_step_id = factory.LazyFunction(lambda: TourStepFactory().id)
    url = None
    upload = factory.LazyAttribute(
        lambda _: FakeFileStorage(BytesIO(CSV_DATA), "step.jpeg")
    )


class TourStepFactory(factories.CKANFactory):
    class Meta:
        model = tour_model.TourStep
        action = "tour_step_create"

    id = factory.Faker("uuid4")
    title = factory.Faker("sentence")
    element = ".dataset-list"
    intro = factory.Faker("sentence")
    position = tour_model.TourStep.Position.bottom
    tour_id = factory.LazyFunction(lambda: TourFactory().id)
    image = factory.LazyAttribute(
        lambda self: [vars(TourStepImageFactory.stub(tour_step_id=self.id))]
    )


class TourFactory(factories.CKANFactory):
    class Meta:
        model = tour_model.Tour
        action = "tour_create"

    id = factory.Faker("uuid4")
    title = factory.Faker("sentence")
    anchor = "#tour-tooltip"
    page = "/dataset"
    author_id = factory.LazyFunction(lambda: factories.User()["id"])  # type: ignore
    steps = factory.LazyAttribute(
        lambda self: [vars(TourStepFactory.stub(tour_id=self.id))]
    )
