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

    switch_last_add_image: GObject.Property = GObject.Property(type=bool, default=False)

    # TODO Singals
    __gsignals__ = {
        "mon-signal": (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    lists_image: Adw.Carousel = Gtk.Template.Child()
    box_lists_image: Gtk.Box = Gtk.Template.Child()
    dots_lists_image: Adw.CarouselIndicatorDots = Gtk.Template.Child()
    main_overlay: Gtk.Box = Gtk.Template.Child()
    delete: Gtk.Button = Gtk.Template.Child()
    download: Gtk.Button = Gtk.Template.Child()
    info: Gtk.Button = Gtk.Template.Child()

    _vertical = False

    def __init__(self):
        super().__init__()

        self.store: Gio.ListStore = None
        self.delete.connect("clicked", lambda _: self.delete_image_selected())
        self.download.connect("clicked", lambda _: self.save_image_selected())


    @GObject.Property
    def vertical(self):
        "Read only property."
        return False

    @GObject.Property(type=bool, default=False)
    def vertical_mode(self):
        "Read-write integer property."
        return self._vertical

    @vertical_mode.setter
    def vertical_mode(self, value):
        self._vertical = value
        if self._vertical:
            self.box_lists_image.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.dots_lists_image.set_orientation(Gtk.Orientation.VERTICAL)
            self.lists_image.set_orientation(Gtk.Orientation.VERTICAL)
        else:
            self.box_lists_image.set_orientation(Gtk.Orientation.VERTICAL)
            self.dots_lists_image.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.lists_image.set_orientation(Gtk.Orientation.HORIZONTAL)


    def set_store(self, store: Gio.ListStore):
        if self.store is None:
            self.store = store
            self.store.connect(
                "items_changed",
                self._on_store_images_changed
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

    def get_image_selected(self) -> ImgData | None:
        if self.store is not None:
            return self.store.get_item(self.lists_image.get_position()).data

        return None

    def save_image_selected(self):
        image = self.get_image_selected()
        if image is None:
            return

        file_dialog = Gtk.FileDialog()
        file_dialog.set_initial_name(f"image.{image.img_format}")
        file_dialog.save(self.get_root(), None, self.on_save_response)

    def delete_image_selected(self):
        if self.store is None:
            return

        self.store.remove(self.lists_image.get_position())

    def _on_store_images_changed(self, _, position, removed, added):
        if added > 0:
            self.append_images(self.store.get_item(position).data)
        elif removed > 0:
            self.lists_image.remove(self.lists_image.get_nth_page(position))

    def on_save_response(self, dialog, res):
        image = self.get_image_selected()
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
