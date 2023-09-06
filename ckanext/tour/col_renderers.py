from __future__ import annotations

from ckanext.toolbelt.decorators import Collector

import ckanext.admin_panel.types as ap_types

renderer, get_renderers = Collector("tour").split()


@renderer
def steps(
    rows: ap_types.ItemList, row: ap_types.Item, value: ap_types.ItemValue, **kwargs
) -> int:
    return len(value)
