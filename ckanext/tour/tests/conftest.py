from io import BytesIO

import pytest
from ckan.lib import uploader
from ckan.tests import factories
from faker import Faker
from pytest_factoryboy import register

import ckanext.tour.tests.factories as tour_factories
from ckanext.tour.tests.helpers import CSV_DATA, FakeFileStorage

fake = Faker()

register(tour_factories.TourFactory, "tour")
register(tour_factories.TourStepFactory, "tour_step")
register(tour_factories.TourStepImageFactory)


def _migrate_plugins(migrate_db_for):
    migrate_db_for("tour")
    migrate_db_for("files")


@pytest.fixture()
def clean_db(with_plugins, reset_db, migrate_db_for):
    reset_db()
    _migrate_plugins(migrate_db_for)


@register
class UserFactory(factories.User):
    pass


@register(_name="sysadmin")
class SysadminFactory(factories.Sysadmin):
    pass


@pytest.fixture
def mock_storage(monkeypatch, ckan_config, tmpdir):
    monkeypatch.setitem(ckan_config, "ckan.storage_path", str(tmpdir))
    monkeypatch.setattr(uploader, "get_storage_path", lambda: str(tmpdir))


# @pytest.fixture
# def rd_study_data(study):
#     def _prepare_data(**kwargs):
#         request_study_id = fake.uuid4()

#         data = {
#             "id": request_study_id,
#             "title": fake.sentence(),
#             "use_main_request": True,
#             "use_main_docs": False,
#             "request_protocol": False,
#             "request_raw": False,
#             "request_clean": False,
#             "request_shareable": False,
#             "package_id": study["id"],
#             "files": [],
#         }
#         data.update(**kwargs)

#         return data

#     yield _prepare_data


@pytest.fixture
def tour_image_data():
    def _prepare_data(**kwargs):
        data = {
            "upload": FakeFileStorage(BytesIO(CSV_DATA), "data.csv"),
            "url": None,
        }

        data.update(**kwargs)

        return data

    yield _prepare_data
