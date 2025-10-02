# states_row.py
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


@Gtk.Template(resource_path='/fr/daemonwhite/Inspira/ui/widgets/states_row.ui')
class StatesRow(Adw.ActionRow):
    __gtype_name__ = 'StatesRow'

    color: Gtk.Box = Gtk.Template.Child()
    icon: Gtk.Image = Gtk.Template.Child()

    def __init__(self, activate: bool=False):
        super().__init__()
        self.__activate = activate

        self.set_active(self.__activate)

    def set_active(self, activate: bool):
        self.__activate = activate

        if self.__activate:
            self.icon.set_from_icon_name("test-pass-symbolic")
            self.color.remove_css_class("error")
            self.color.add_css_class("success")
        else:
            self.icon.set_from_icon_name("minus-large-circle-outline-symbolic")
            self.color.remove_css_class("success")
            self.color.add_css_class("error")
