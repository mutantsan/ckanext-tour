from __future__ import annotations

from flask import Blueprint

import ckan.plugins.toolkit as tk
from flask.views import MethodView

from ckanext.ap_main.views.generics import ApConfigurationPageView
from ckanext.ap_main.utils import ap_before_request

tour = Blueprint("tour_config", __name__)
tour.before_request(ap_before_request)
