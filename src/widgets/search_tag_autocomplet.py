# search_tag_autocomplet.py
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

from gi.repository import Gtk

from config import URI_PATH


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/search_tag_autocomplet.ui')
class SearchTagAutocomplet(Gtk.SearchEntry):
    __gtype_name__ = 'SearchTagAutocomplet'

    popover: Gtk.Popover = Gtk.Template.Child()
    popover_list: Gtk.ListView = Gtk.Template.Child()

    def __init__(self,):
        super().__init__()

        self.connect("search-changed", self.on_search_changed)

        self.tags = ['teste']

        self.string_list = Gtk.StringList.new(self.tags)
        self.selection = Gtk.SingleSelection.new(self.string_list)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.on_setup)
        factory.connect("bind", self.on_bind)

        self.popover_list.set_model(self.selection)
        self.popover_list.set_factory(factory)
        self.popover_list.connect("activate", self.on_row_activated)

    def add_tags(self, tags: list[str]):
        for tag in tags:
            self.tags.append(tag)

    def get_searched_tag(self) -> list[str]:
        tags: list = []

        for tag in self.get_text().rsplit(","):
            tags.append(tag.strip())

        return tags

    def on_setup(self, factory, item: Gtk.ListItem):
        item.set_child(Gtk.Label(xalign=0))

    def on_bind(self, factory, item):
        label = item.get_child()
        string_object = item.get_item()
        label.set_text(string_object.get_string())

    def get_tag_edit_position(self) -> list[int]:
        search_text = self.get_text().lower()
        list_text: list = search_text.rsplit(",")

        start_pos: int = 0
        end_pos: int = 0

        position = self.get_position()

        for frag_text in list_text:
            end_pos: int = start_pos + len(frag_text)

            if end_pos >= position:
                break

            start_pos += len(frag_text) + 1

        return [start_pos, end_pos]

    def on_search_changed(self, search_entry):
        pos = self.get_tag_edit_position()
        text = self.get_text().lower()[pos[0]:pos[1]].strip()

        if text:
            filtered = [w for w in self.tags if text in w.lower()]
            self.string_list.splice(
                0, self.string_list.get_n_items(), filtered
            )

            if filtered and filtered[0].lower() != text:
                self.popover.popup()
            else:
                self.popover.popdown()
        else:
            self.popover.popdown()

    def on_row_activated(self, listview, pos):
        item = self.string_list.get_item(pos)
        text = self.get_text()
        pos = self.get_tag_edit_position()

        self.set_text(text[:pos[0]] + item.get_string() + text[pos[1]:])
        self.set_position(pos[0] + len(item.get_string())+1)

        self.popover.popdown()
