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

from enum import Enum

from gi.repository import Gtk, Adw, GObject

from config import URI_PATH


class RowState(Enum):
    ERROR = 0
    WARNING = 1
    SUCCESS = 2
    NEUTRAL = -1


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/states_row.ui')
class StatesRow(Adw.ActionRow):
    __gtype_name__ = 'StatesRow'

    color: Gtk.Box = Gtk.Template.Child()
    icon: Gtk.Image = Gtk.Template.Child()

    _state = -1

    def __init__(self, activate: bool = False):
        super().__init__()
        self._update_state()

    @GObject.Property(type=int)
    def state(self) -> RowState:
        return RowState(self._state)

    @state.setter
    def state(self, value):
        self._state = value
        if self.do_realize:
            self._update_state()

    def _update_state(self):
        state = self.state
        icon = ""
        css_class = ""

        CSS_LIST = [
            "error",
            "warning",
            "success",
            "neutral"
        ]

        for css in CSS_LIST:
            self.color.remove_css_class(css)

        if state == RowState.ERROR:
            css_class = "error"
            icon = "minus-large-circle-outline-symbolic"
        elif state == RowState.WARNING:
            css_class = "warning"
            icon = "warning-outline-symbolic"
        elif state == RowState.SUCCESS:
            css_class = "success"
            icon = "test-pass-symbolic"
        elif state == RowState.NEUTRAL:
            css_class = "neutral"
            icon = "info-outline-symbolic"

        self.color.add_css_class(css_class)
        self.icon.set_from_icon_name(icon)
