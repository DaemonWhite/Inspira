# info_images.py
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

from gi.repository import Gtk, Adw

from config import URI_PATH

from ..core.Api import ImgData
from .wrap_tags import WrapTags
from .states_row import StatesRow, RowState


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/infos_image.ui')
class InfosImage(Adw.Bin):
    __gtype_name__ = 'InfosImage'

    nswf_image_row: StatesRow = Gtk.Template.Child()
    url_image_row: Adw.ActionRow = Gtk.Template.Child()
    autor_image_row: Adw.ActionRow = Gtk.Template.Child()
    tags_image_row: WrapTags = Gtk.Template.Child()
    len_tags_image_row: Gtk.Label = Gtk.Template.Child()

    tags_api_row: WrapTags = Gtk.Template.Child()
    len_tags_api_row: Gtk.Label = Gtk.Template.Child()

    api_tag_row: Adw.ActionRow = Gtk.Template.Child()
    nswf_tag_row: Adw.ActionRow = Gtk.Template.Child()

    def __init__(self,):
        super().__init__()

    def set_infos_image(self, image_data: ImgData):
        self.clear()

        # InfosImage
        self.nswf_image_row.state = self.__state_row_nsfw(image_data.nsfw)
        self.url_image_row.set_subtitle(image_data.url)
        self.autor_image_row.set_subtitle(image_data.author)

        self.tags_image_row.add_tags(image_data.img_tags)

        self.len_tags_image_row.set_label(
            f"{len(image_data.img_tags)}"
        )

        # InfosApi

        self.api_tag_row.set_title(image_data.api_name)
        self.nswf_tag_row.state = self.__state_row_nsfw(image_data.request.nsfw)

        self.tags_api_row.add_tags(image_data._info_request.search_tags)

        self.len_tags_api_row.set_label(
            f"{len(image_data.request.search_tags)}"
        )

    def clear(self):
        # InfosImage
        self.nswf_image_row.state = self.__state_row_nsfw(False)
        self.url_image_row.set_subtitle("")
        self.autor_image_row.set_subtitle("")
        self.tags_image_row.remove_all()
        self.len_tags_image_row.set_label("0")

        # InfosApi
        self.nswf_tag_row.state = self.__state_row_nsfw(False)
        self.tags_api_row.remove_all()
        self.len_tags_api_row.set_label("0")

    def __state_row_nsfw(self, is_nsfw: bool) -> RowState:
        state = RowState.ERROR.value
        if is_nsfw:
            state = RowState.SUCCESS.value
        return state
