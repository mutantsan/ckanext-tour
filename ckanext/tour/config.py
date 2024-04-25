import ckan.plugins.toolkit as tk

CONF_AUTOPLAY = "ckanext.tour.autoplay"
CONF_DEFAULT_ANCHOR = "ckanext.tour.default_anchor"
CONF_COLLAPSE_STEPS = "ckanext.tour.collapse_steps"


def is_auto_play_enabled() -> bool:
    return tk.config[CONF_AUTOPLAY]


def get_default_anchor() -> str:
    return tk.config[CONF_DEFAULT_ANCHOR]


def is_collapse_steps_enabled() -> bool:
    return tk.config[CONF_COLLAPSE_STEPS]
