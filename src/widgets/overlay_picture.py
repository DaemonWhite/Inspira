# overlay_picture.py
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

from gi.repository import Adw, Gtk, GLib, Gdk, Gio, GObject

from config import URI_PATH

from ..core.imgData import ImgData


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/overlay_picture.ui')
class OverlayPicture(Gtk.Overlay):
    __gtype_name__ = "OverlayPicture"

    switch_last_add_image = GObject.Property(type=bool, default=False)

    # TODO Singals
    __gsignals__ = {
        "mon-signal": (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    lists_image: Adw.Carousel = Gtk.Template.Child()
    main_overlay: Gtk.Box = Gtk.Template.Child()
    download: Gtk.Button = Gtk.Template.Child()
    info: Gtk.Button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.store: Gio.ListStore = None
        self.download.connect("clicked", lambda _: self.save_image())

    def set_store(self, store: Gio.ListStore):
        if self.store is None:
            self.store = store
            self.store.connect(
                "items_changed",
                lambda _store, position, _removed, _added : self.append_images(
                    self.store.get_item(position).data
                )
            )

    def append_images(self, image_data: ImgData):
        bytes_data = GLib.Bytes.new(image_data.img)
        texture = Gdk.Texture.new_from_bytes(bytes_data)
        self.lists_image.append(Gtk.Picture.new_for_paintable(texture))

        if self.switch_last_add_image:
            pos = self.lists_image.get_n_pages() - 1
            self.lists_image.scroll_to(
                self.lists_image.get_nth_page(pos), True
            )
        elif self.lists_image.get_n_pages() == 1:
            self.lists_image.scroll_to(
                self.lists_image.get_nth_page(0), True
            )

    def save_image(self):
        image = self.store.get_item(self.lists_image.get_position()).data
        file_dialog = Gtk.FileDialog()
        file_dialog.set_initial_name(f"image.{image.img_format}")
        file_dialog.save(self.get_root(), None, self.on_save_response)

    def on_save_response(self, dialog, res):
        image = self.store.get_item(self.lists_image.get_position()).data
        try:
            file = dialog.save_finish(res)
            if file:
                path = file.get_path()
                if path:
                    with open(path, "wb") as f:
                        f.write(image.img)
                    print(f"Img save in {path}")
        except Exception as e:
            print("Save cancel or error :", e)
