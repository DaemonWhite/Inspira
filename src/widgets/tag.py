# tag.py
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


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/tag.ui')
class Tag(Gtk.Box):
    __gtype_name__ = 'Tag'

    tag_name: Gtk.Label = Gtk.Template.Child()
    close: Gtk.Button = Gtk.Template.Child()

    def __init__(self, label: str):
        super().__init__()
        self.tag_name.set_label(label)

