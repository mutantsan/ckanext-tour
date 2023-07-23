from __future__ import annotations

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from ckanext.admin_panel.interfaces import IAdminPanel
from ckanext.admin_panel.types import SectionConfig, ConfigurationItem


@tk.blanket.helpers
@tk.blanket.actions
@tk.blanket.auth_functions
@tk.blanket.blueprints
class TourPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(IAdminPanel)

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
                    ConfigurationItem(
                        name="Global settings",
                        blueprint="tour.list",
                    ),
                    ConfigurationItem(
                        name="Manage tours",
                        blueprint="tour.list",
                        info="Manage existing tours",
                    ),
                    ConfigurationItem(
                        name="Add tour",
                        blueprint="user.index",
                        info="Add new tour",
                    ),
                ],
            )
        )
        return config_list
