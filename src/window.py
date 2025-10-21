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

import threading

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gio

from config import devel, URI_PATH, OS

from .items.image import ImageItem

from .core import Api, Manager
from .core.Api import ImgData

from .widgets.infos_image import InfosImage
from .widgets.notif_button import NotifButton
from .widgets.overlay_picture import OverlayPicture
from .widgets.search_tag_autocomplet import SearchTagAutocomplet
from .widgets.wrap_tags import WrapTags


@Gtk.Template(resource_path=URI_PATH+'/ui/window.ui')
class InspiraWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'InspiraWindow'

    search_box: Gtk.Box = Gtk.Template.Child()
    search_nsfw: Adw.ToggleGroup = Gtk.Template.Child()
    search_tags_entry: SearchTagAutocomplet = Gtk.Template.Child()
    search_add_tags: Gtk.Button = Gtk.Template.Child()
    wrap_tags: WrapTags = Gtk.Template.Child()

    image: OverlayPicture = Gtk.Template.Child()
    image_box: Gtk.Box = Gtk.Template.Child()
    image_drop_down: Gtk.DropDown = Gtk.Template.Child()

    search_view: Adw.OverlaySplitView = Gtk.Template.Child()

    notif_download: NotifButton = Gtk.Template.Child()

    overlay_image: Adw.OverlaySplitView = Gtk.Template.Child()
    infos_image: InfosImage = Gtk.Template.Child()

    key_action: Gio.Menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = self.get_application()
        self.manager:  Manager.Api = self.app.manager

        self.app.create_action(
            'newpicture',
            self.on_load_image,
            ['<primary><shift>r']
        )

        self.create_action(
            'togglesearchview',
            self._on_toggle_search_view,
            ['F9']
        )

        shotcut_menu_action = "app.shortcuts"

        if OS == "windows":
            shotcut_menu_action = "win.show-help-overlay"

        self.key_action.insert_item(
            1,
            Gio.MenuItem.new(_("_Keyboard Shortcuts"), shotcut_menu_action)
        )

        self.bind_events()
        self.image.set_store(self.app.store_images)

        self.search_add_tags.connect("clicked", self._on_add_tags)

        if devel:
            self.add_css_class("devel")

        self.api_store = Gio.ListStore.new(Gtk.StringObject)

        self._on_load_api()
        self.app.connect("loaded_api", lambda _: self._on_load_api())

        self.search_tags_entry.add_tags(self.manager.get_all_tags())

        self.select_view_capability_api()

        self.is_nsfw_enabled()
        self.asyncLoadImage()

    def bind_events(self):
        self.image_drop_down.connect(
            "notify::selected",
            lambda _widget, _param: self.select_view_capability_api()
        )

        self.image.info.connect("clicked", self.on_view_info_image)
        self.image.lists_image.connect(
            "page_changed", lambda _, index: self.infos_image.set_infos_image(
                self.app.store_images.get_item(index).data
            )
        )
        self.app.settings.bind(
            "switch-last-add-image",
            self.image,
            "switch_last_add_image",
            Gio.SettingsBindFlags.GET
        )

        self.app.settings.bind(
            "carousel-images-is-vertical",
            self.image,
            "vertical_mode",
            Gio.SettingsBindFlags.GET
        )

        self.app.download_manager.end_queue.connect(
            "items-changed",
            self.on_download_image
        )

        self.connect(
            "close-request",
            lambda _: self.app.download_manager.shutdown()
        );

        self.notif_download.connect_download_manager(self.app.download_manager)

    def _on_toggle_search_view(self, action, _):
        self.search_view.set_show_sidebar(
            not self.search_view.get_show_sidebar()
        )

    def _on_load_api(self):
        self.api_store.remove_all()
        for plugin in self.manager.list_plugins():
            if plugin["active"]:
                self.api_store.append(Gtk.StringObject.new(plugin["name"]))

        self.image_drop_down.set_model(self.api_store)

    def _on_add_tags(self, _):
        self.wrap_tags.add_tags(self.search_tags_entry.get_searched_tag())

    def on_load_image(self, widget, _):
        self.asyncLoadImage()

    def on_view_info_image(self, widget):
        self.overlay_image.set_show_sidebar(
            not self.overlay_image.get_show_sidebar()
        )

    def on_download_image(self, model: Gio.ListStore, position, remove, added):
        if added < 1:
            return
        imgs: Api.ImgData = model.get_item(position).imgs

        for img in imgs:
            if img.success:
                GLib.idle_add(self._updateImage, img)
            else:
                print(img.error)

    def select_view_capability_api(self):
        if self.image_drop_down.get_model().get_n_items() < 1:
            print("Error not api available")
            return
        selected_api = self.image_drop_down.get_selected_item().get_string()
        api: Api.ApiInterface = self.manager.get_plugin(selected_api)

        # Random or serach
        capability_mode = api.randomCapability

        self.search_tags_entry.set_visible(capability_mode.tag.present)
        self.search_add_tags.set_visible(capability_mode.tag.present)
        self.wrap_tags.set_visible(capability_mode.tag.present)

        if self.app.settings.global_nsfw:
            self.search_nsfw.set_visible(capability_mode.nsfw)
        else:
            self.search_nsfw.set_visible(False)
            self.search_nsfw.set_active_name("sfw")

    def is_nsfw_enabled(self) -> bool:
        if "nsfw" == self.search_nsfw.get_active_name():
            return True
        return False

    def loadImage(self, args):
        if self.image_drop_down.get_model().get_n_items() < 1:
            print("Error not api available")
            return
        selected_api = self.image_drop_down.get_selected_item().get_string()

        data = self.manager.random(
            selected_api,
            nsfw=self.is_nsfw_enabled(),
            tags=self.wrap_tags.get_tags()
        )
        if not data.success > 0:
            print("request failled : ", data)
            return

        self.app.download_manager.append(data)

    def _updateImage(self, content):
        try:
            self.app.store_images.append(ImageItem(content))
        except GLib.GError as e:
            print(f"Error load image: {e}")

    def asyncLoadImage(self, args=None):
        t = threading.Thread(target=self.loadImage, args=[args])
        t.start()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.app.set_accels_for_action(f"win.{name}", shortcuts)

