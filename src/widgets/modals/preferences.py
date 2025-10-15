# window.py
#
# Copyright 2025 DaemonWhite
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

from ...utils.load_apis import save_config_api

from config import URI_PATH

from ...core import Manager
from ..switch_info_row import SwitchInfoRow

from ...utils.gtk_settings import InspiraSettings


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/modals/preferences.ui')
class PreferencesModal(Adw.PreferencesDialog):
    __gtype_name__ = "PreferencesModal"

    global_nsfw: Adw.SwitchRow = Gtk.Template.Child()

    switch_last_add_image: Adw.SwitchRow = Gtk.Template.Child()
    carousel_image: Adw.SwitchRow = Gtk.Template.Child()

    timeout_spin: Adw.SpinRow = Gtk.Template.Child()
    auto_save_tags_switch: Adw.SwitchRow = Gtk.Template.Child()

    apis_group: Adw.PreferencesGroup = Gtk.Template.Child()
    tags_group: Adw.PreferencesGroup = Gtk.Template.Child()
    ## TODO Create Tags Manager

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.__app = app
        self.__manager: Manager.Api = app.manager
        self.__settings: InspiraSettings = app.settings
        self.connect("closed", self.on_close_request)

        self._binding()

        self._load_apis()
        self._load_tags()

    def _binding(self):
        self.__settings.bind(
            "auto-save-tags",
            self.auto_save_tags_switch,
            "active",
            Gio.SettingsBindFlags.DEFAULT
        )

        self.__settings.bind(
            "global-nsfw",
            self.global_nsfw,
            "active",
            Gio.SettingsBindFlags.DEFAULT
        )

        self.__settings.bind(
            "carousel-images-is-vertical",
            self.carousel_image,
            "active",
            Gio.SettingsBindFlags.DEFAULT
        )

        self.__settings.bind(
            "switch-last-add-image",
            self.switch_last_add_image,
            "active",
            Gio.SettingsBindFlags.DEFAULT
        )

        self.__settings.bind(
            "timeout-download",
            self.timeout_spin,
            "value",
            Gio.SettingsBindFlags.DEFAULT
        )

    def _load_apis(self):
        for api in self.__manager.list_plugins():
            api_row = SwitchInfoRow()
            api_row.set_title(title=api['name'])
            api_row.set_active(api['active'])

            if api["capabilities"]["random"].present:
                api_row.create_tag(_("Random"))

            if api["capabilities"]["search"].present:
                api_row.create_tag(_("Search"))

            api_row.connect("activated", self.on_switch_api)

            self.apis_group.add(api_row)

    def on_switch_api(self, switch_api: Adw.SwitchRow, state):
        if switch_api.get_active():
            self.__manager.enable(
                switch_api.get_title(),
            )
        else:
            self.__manager.disable(
                switch_api.get_title(),
            )

    def _load_tags(self):
        pass

    def on_close_request(self, _):
        save_config_api(self.__manager.list_plugins())
        self.__app.load_apis()
