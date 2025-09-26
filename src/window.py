# window.py
#
# Copyright 2025 Mathéo
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

from .interfaceAPI.nekomoe import NekoMoe


@Gtk.Template(resource_path='/fr/daemonwhite/Inspira/ui/window.ui')
class InspiraWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'InspiraWindow'

    image = Gtk.Template.Child()
    work_box = Gtk.Template.Child()
    work_spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_application().create_action('newpicture', self.on_load_image)

        self._neko = NekoMoe()
        self.asyncLoadImage()

    def on_load_image(self, widget, _):
        self.asyncLoadImage()

    def loadImage(self, args):
        data = self._neko.random([""])
        content = self._neko.download(data)

        if content is not None:
            GLib.idle_add(self._updateImage, content)

    def loadedImage(self):
        self.work_box.set_visible(False)
        self.image.set_visible(True)

    def _updateImage(self, content):
        try:
            bytes_data = GLib.Bytes.new(content)
            texture = Gdk.Texture.new_from_bytes(bytes_data)
            self.image.set_from_paintable(texture)
            self.image.set_pixel_size(self.get_allocated_width())
        except GLib.GError as e:
            print(f"Error load image: {e}")

        self.loadedImage()

    def asyncLoadImage(self, args=None):
        self.work_box.set_visible(True)
        self.image.set_visible(False)
        t = threading.Thread(target=self.loadImage, args=[args])
        t.start()
