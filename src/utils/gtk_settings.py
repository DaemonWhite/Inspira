# gtk_settings.py
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

from gi.repository import Gio
from config import URI


class InspiraSettings(Gio.Settings):

    def __init__(self,):
        super().__init__(URI)

    @property
    def auto_save_tags(self) -> bool:
        return self.get_boolean("auto-save-tags")

    @auto_save_tags.setter
    def auto_save_tags(self, enable: bool):
        self.set_boolean("auto-save-tags")

    @property
    def global_nsfw(self) -> bool:
        return self.get_boolean("global-nsfw")

    @global_nsfw.setter
    def global_nsfw(self, enable: bool):
        self.set_boolean("global-nsfw")

    @property
    def timeout_download(self) -> int:
        return self.get_int("timeout-download")

    @timeout_download.setter
    def timeout_download(self, value: bool):
        self.set_int("timeout-download", value)
