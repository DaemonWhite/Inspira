# notif_button.py
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject

from config import URI_PATH

from ..core.Api import ImgData
from ..core.Manager import DownloadItemStates, DownloadManager

from ..utils.state_progress import StateProgress

from .state_progress_row import StatesProgressRow


@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/notif_button.ui')
class NotifButton(Gtk.Button):
    __gtype_name__ = "NotifButton"

    notif_spinner: Adw.Spinner = Gtk.Template.Child()
    notif_state: Gtk.Image = Gtk.Template.Child()
    notif_popup: Gtk.Popover = Gtk.Template.Child()
    notif_list: Gtk.ListBox = Gtk.Template.Child()

    _state = 2

    def __init__(self):
        super().__init__()
        self.notif_spinner.set_visible(False)
        self.connect("clicked", self._on_button)

        self._update_state()

    @GObject.Property(type=int)
    def state(self) -> StateProgress:
        return StateProgress(self._state)

    @state.setter
    def state(self, value):
        self._state = value
        print(value)
        if self.get_realized():
            self._update_state()

    def connect_download_manager(self, download_manager: DownloadManager):
        download_manager.connect("notify::downloading", self._on_donwloading)
        download_manager.queue.connect("items_changed", self._on_add_items)

    def _on_donwloading(self, download_manager: DownloadManager, _):
        self.notif_spinner.set_visible(download_manager.downloading)
        self.notif_state.set_visible(not download_manager.downloading)

    def _on_add_items(self, model, position, removed, added):
        if added < 1:
            return

        item: DownloadItemStates = model.get_item(position)

        row = StatesProgressRow()
        row.set_title(item.data.api_name)
        self._on_progress_download(item, row)
        row.state = item.status.value

        item.connect(
            "notify::status",
            lambda item, _: self._on_status_download(item, row)
        )

        item.connect(
            "notify::progress",
            lambda item, _: self._on_progress_download(item, row)
        )

        self.notif_list.prepend(row)


    def _on_button(self, _widget):
        self.notif_popup.popup()

    def _on_status_download(self, item: DownloadItemStates, row: StatesProgressRow):
        row.state = item.status.value

    def _on_progress_download(self, item: DownloadItemStates, row: StatesProgressRow):
        row.set_subtitle(f"{item.progress}/{item.length}")

    def _update_state(self):
        state = self.state
        if state == StateProgress.DOWNLOADING:
            self.notif_spinner.set_visible(True)
            self.notif_state.set_visible(False)
        elif state == StateProgress.WARNING:
            self.notif_spinner.set_visible(False)
            self.notif_state.set_visible(True)
            self.notif_state.set_from_icon_name("warning-outline-symbolic")
        elif state == StateProgress.SUCCESS:
            self.notif_spinner.set_visible(False)
            self.notif_state.set_visible(True)
            self.notif_state.set_from_icon_name("test-pass-symbolic")
