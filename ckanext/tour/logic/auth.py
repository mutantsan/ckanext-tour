import ckan.plugins.toolkit as tk


@tk.auth_allow_anonymous_access
def tour_get_sum(context, data_dict):
    return {"success": True}


def get_auth_functions():
    return {
        "tour_get_sum": tour_get_sum,
    }
