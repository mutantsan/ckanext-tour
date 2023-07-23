"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.tour.logic import validators


def test_tour_reauired_with_valid_value():
    assert validators.tour_required("value") == "value"


def test_tour_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.tour_required(None)
