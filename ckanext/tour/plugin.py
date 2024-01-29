from __future__ import annotations

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from ckanext.collection.interfaces import ICollection, CollectionFactory

from ckanext.ap_main.interfaces import IAdminPanel
from ckanext.ap_main.types import ConfigurationItem, SectionConfig

from ckanext.tour.collection import TourListCollection


@tk.blanket.helpers
@tk.blanket.actions
@tk.blanket.auth_functions
@tk.blanket.blueprints
@tk.blanket.validators
class TourPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(IAdminPanel, inherit=True)
    plugins.implements(ICollection, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "tour")

    # IAdminPanel

    def register_config_sections(
        self, config_list: list[SectionConfig]
    ) -> list[SectionConfig]:
        config_list.append(
            SectionConfig(
                name="Tour",
                configs=[
                    # ConfigurationItem(
                    #     name="Global settings",
                    #     blueprint="tour.config",
                    #     info="Global configuration for a tour",
                    # ),
                    ConfigurationItem(
                        name="List of tours",
                        blueprint="tour.list",
                        info="Manage existing tours",
                    ),
                    ConfigurationItem(
                        name="Add tour",
                        blueprint="tour.add",
                        info="Add new tour",
                    ),
                ],
            )
        )
        return config_list

    # ICollection

    def get_collection_factories(self) -> dict[str, CollectionFactory]:
        return {"tour-list": TourListCollection}
