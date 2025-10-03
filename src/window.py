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
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gio

from config import devel

from .widgets.infos_image import InfosImage
from .widgets.overlay_picture import OverlayPicture
from .widgets.search_tag_autocomplet import SearchTagAutocomplet
from .widgets.wrap_tags import WrapTags


@Gtk.Template(resource_path='/fr/daemonwhite/Inspira/ui/window.ui')
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

    overlay_image: Adw.OverlaySplitView = Gtk.Template.Child()
    infos_image: InfosImage = Gtk.Template.Child()

    work_box: Gtk.Box = Gtk.Template.Child()
    work_spinner: Adw.Spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = self.get_application()
        self.lock_load_image = False
        self.app.create_action(
            'newpicture',
            self.on_load_image,
            ['<primary>r']
        )

        self.bind_events()

        self.search_add_tags.connect("clicked", self._on_add_tags)

        if devel:
            self.add_css_class("devel")

        self.store = Gio.ListStore.new(Gtk.StringObject)
        for plugin in self.app.manager.list_plugins():
            if plugin["active"]:
                self.store.append(Gtk.StringObject.new(plugin["name"]))

        self.search_tags_entry.add_tags(self.app.manager.get_all_tags())

        self.image_drop_down.set_model(self.store)
        self.is_nsfw_enabled()
        self.asyncLoadImage()

    def bind_events(self):
        self.image.info.connect("clicked", self.on_view_info_image)

    def _on_add_tags(self, _):
        self.wrap_tags.add_tags(self.search_tags_entry.get_searched_tag())

    def on_load_image(self, widget, _):
        self.asyncLoadImage()

    def on_view_info_image(self, widget):
        self.overlay_image.set_show_sidebar(
            not self.overlay_image.get_show_sidebar()
        )

    def is_nsfw_enabled(self) -> bool:
        if "nsfw" == self.search_nsfw.get_active_name():
            return True
        return False

    def loadImage(self, args):
        selected_api = self.image_drop_down.get_selected_item().get_string()

        data = self.app.manager.random(
            selected_api,
            nsfw=self.is_nsfw_enabled(),
            tags=self.wrap_tags.get_tags()
        )

        if data.success:
            imgs = data.extact_imgs_request()
            self.infos_image.set_infos_image(imgs[0])
            imgs[0].download()
            if imgs[0].success:
                GLib.idle_add(self._updateImage, imgs[0])
            else:
                self.loadedImage()
                print(imgs[0].error)
        else:
            self.loadedImage()
            print(data.error)

    def loadedImage(self):
        self.work_box.set_visible(False)
        self.image_box.set_visible(True)
        self.search_box.set_sensitive(True)
        self.lock_load_image = False

    def _updateImage(self, content):
        try:
            self.image.set_image(content)
        except GLib.GError as e:
            print(f"Error load image: {e}")

        self.loadedImage()

    def asyncLoadImage(self, args=None):
        if self.lock_load_image:
            return None

        self.lock_load_image = True
        self.work_box.set_visible(True)
        self.image_box.set_visible(False)
        self.search_box.set_sensitive(False)
        t = threading.Thread(target=self.loadImage, args=[args])
        t.start()
