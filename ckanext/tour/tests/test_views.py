"""Tests for views.py."""

import pytest

import ckanext.tour.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "tour")
@pytest.mark.usefixtures("with_plugins")
def test_tour_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("tour.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, tour!"
