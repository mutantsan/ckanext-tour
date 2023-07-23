import ckan.plugins.toolkit as tk
import ckanext.tour.logic.schema as schema


@tk.side_effect_free
def tour_list(context, data_dict):
    tk.check_access(
        "tour_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.tour_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return []
