import pytest

import ckan.plugins.toolkit as tk
from ckan.tests.helpers import call_action


@pytest.mark.usefixtures("with_plugins", "clean_db", "validation_setup")
class TestTourCreate:
    def test_basic_create(self, tour_factory):
        tour = tour_factory()

        pass


    # def test_create_without_studies(self, user):
    #     with pytest.raises(
    #         tk.ValidationError, match="Cannot create a data request without studies"
    #     ):
    #         call_action(
    #             "msf_rd_data_request_create",
    #             author_id=user["id"],
    #         )

    # def test_create_no_files_at_all(
    #     self,
    #     data_request_factory,
    #     rd_study_data,
    # ):
    #     """If we are creating a data request without main docs, each study must
    #     contain uploaded files"""

    #     with pytest.raises(
    #         tk.ValidationError,
    #         match="Main docs are empty, but one or more studies relies on it",
    #     ):
    #         data_request_factory(files=[], studies=[
    #                              rd_study_data(use_main_docs=True)])

    #     data_request_factory(studies=[rd_study_data(use_main_docs=True)])


# @pytest.mark.usefixtures("with_plugins", "clean_db", "validation_setup")
# class TestDataRequestUpdateStatus:
#     def test_not_exist(self):
#         with pytest.raises(
#             tk.ValidationError,
#             match="The data request with an id xxx doesn't exist",
#         ):
#             call_action("msf_rd_data_request_update_status", id="xxx")

#     def test_change_to_wrong_status(self, data_request):
#         with pytest.raises(
#             tk.ValidationError,
#             match="Value must be one of",
#         ):
#             call_action(
#                 "msf_rd_data_request_update_status",
#                 id=data_request["id"],
#                 status="closed",
#             )

#     def test_change_resolved_status(self, data_request):
#         result = call_action(
#             "msf_rd_data_request_update_status",
#             id=data_request["id"],
#             status=DataRequest.Status.resolved,
#         )

#         assert result["status"] == DataRequest.Status.resolved

#         with pytest.raises(
#             tk.ValidationError,
#             match="Can't update resolved data request",
#         ):
#             call_action(
#                 "msf_rd_data_request_update_status",
#                 id=data_request["id"],
#                 status=DataRequest.Status.requested,
#             )


# @pytest.mark.usefixtures(
#     "with_request_context",
#     "clean_db",
#     "with_plugins",
#     "validation_setup",
# )
# class TestDataRequestList:
#     def test_empty_list(self, app, sysadmin):
#         result = call_action(
#             "msf_rd_data_request_list", {
#                 "user": sysadmin["name"], "ignore_auth": False}
#         )

#         assert not result

#     def test_sysadmin_see_all(self, app, sysadmin, data_request):
#         result = call_action(
#             "msf_rd_data_request_list", {
#                 "user": sysadmin["name"], "ignore_auth": False}
#         )

#         assert len(result) == 1
#         assert result[0]

#     def test_not_sysadmin_see_only_their_requests(
#         self, app, user_factory, data_request_factory
#     ):
#         user1 = user_factory()
#         user2 = user_factory()

#         data_request_factory(author_id=user1["id"])
#         data_request_factory(author_id=user2["id"])

#         result = call_action(
#             "msf_rd_data_request_list", {
#                 "user": user1["name"], "ignore_auth": False}
#         )

#         assert len(result) == 1
#         assert result[0]["author"] == user1["id"]
#         assert result[0]["comments"] is None
#         assert isinstance(result[0]["author"], str)

#     def test_with_extras(self, sysadmin, data_request):
#         result = call_action(
#             "msf_rd_data_request_list",
#             {"user": sysadmin["name"], "ignore_auth": False},
#             with_comments=True,
#             with_extras=True,
#         )

#         assert isinstance(result[0]["comments"], list)
#         assert isinstance(result[0]["author"], dict)


# class TestDataRequestDelete:
#     """Seems like the client doesn't want to allow deleting the data request.
#     But if it's going to happen some day, note:
#     - you have to delete a file uploaded via ckanext-files
#     - you have to revoke an access from a user (probably will be revoked auto
#     matically, because the permission function must check for the resolved
#     data request that include the specific study? I don't know yet.)"""
#     pass
