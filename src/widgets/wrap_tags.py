# wrap_tags.py
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

from gi.repository import Gtk, Adw, GLib, GObject

from config import URI_PATH, OS

from .tag import Tag


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/wrap_tags.ui')
class WrapTags(Adw.WrapBox):
    __gtype_name__ = 'WrapTags'
    _tag_removable = True
    def __init__(self,):
        super().__init__()
        self._know_tags = []
        self._ref_tags = []

    @GObject.Property(type=bool, default=True)
    def tag_removable(self):
        return self._tag_removable

    @tag_removable.setter
    def tag_removable(self, value: bool):
        self._tag_removable = value
        for tag in self._ref_tags:
            tag.removable = self._tag_removable
        self.notify('tag_removable')

    def add_tag(self, tag_name: str):
        tag = Tag(label=tag_name, removable = self.tag_removable)
        tag.close.connect("clicked", self._remove_tag, tag)
        if tag_name not in self._know_tags and len(tag_name) > 1:
            self.append(tag)
            self._know_tags.append(tag_name)
            self._ref_tags.append(tag)

    def add_tags(self, tags_names: list[str]):
        for tag_name in tags_names:
            self.add_tag(tag_name)

    def _remove_tag(self, _n, tag: Tag):
        tag_name = tag.tag_name.get_label()
        try:
            self._know_tags.remove(tag_name)
            self._ref_tags.remove(tag)
        except ValueError as e:
            print(f"WARNING: {e} x={tag.tag_name.get_label()} not exist ")

        self.remove(tag)

    def remove_all(self):
        if "linux" == OS:
            super().remove_all()
        else:
            for tag in self._ref_tags:
                self.remove(tag)

        self._know_tags.clear()
        self._ref_tags.clear()

    def get_tags(self) -> list[str]:
        return self._know_tags.copy()
