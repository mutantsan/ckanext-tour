"""Tests for helpers.py."""

import ckanext.tour.helpers as helpers


def test_tour_hello():
    assert helpers.tour_hello() == "Hello, tour!"
