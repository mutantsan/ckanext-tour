from __future__ import annotations

import ckanext.ap_main.types as ap_types
from ckanext.toolbelt.decorators import Collector

renderer, get_renderers = Collector("tour").split()


@renderer
def steps(
    rows: ap_types.ItemList, row: ap_types.Item, value: ap_types.ItemValue, **kwargs
) -> int:
    return len(value)
