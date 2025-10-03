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

from gi.repository import Gtk, GLib, Gdk

from config import URI_PATH

from ..core.imgData import ImgData


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/overlay_picture.ui')
class OverlayPicture(Gtk.Overlay):
    __gtype_name__ = "OverlayPicture"

    image: Gtk.Picture = Gtk.Template.Child()
    main_overlay: Gtk.Box = Gtk.Template.Child()
    download: Gtk.Button = Gtk.Template.Child()
    info: Gtk.Button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.__image: ImgData = None

        self.download.connect("clicked", lambda _: self.save_image())

    def set_image(self, image_data: ImgData):
        bytes_data = GLib.Bytes.new(image_data.img)
        texture = Gdk.Texture.new_from_bytes(bytes_data)
        self.__image = image_data
        self.image.set_paintable(texture)

    def save_image(self):
        if self.__image is None:
            return

        file_dialog = Gtk.FileDialog()
        file_dialog.set_initial_name("image.png")
        file_dialog.save(self.get_root(), None, self.on_save_response)

    def on_save_response(self, dialog, res):
        try:
            file = dialog.save_finish(res)
            if file:
                path = file.get_path()
                if path:
                    with open(path, "wb") as f:
                        f.write(self.__image.img)
                    print(f"Img save in {path}")
        except Exception as e:
            print("Save cancel or error :", e)
