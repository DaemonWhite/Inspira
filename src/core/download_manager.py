# download_manager.py
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
from gi.repository import Gio, GObject

from ..utils.state_progress import StateProgress

from .imgData import ImgData
from .infoRequest import InfoRequest


class DownloadItemStates(GObject.GObject):
    data = GObject.Property(type=object)
    status = GObject.Property(type=object)
    length = GObject.Property(type=int)
    imgs = GObject.Property(type=object)

    def __init__(self, info_request: InfoRequest):
        super().__init__()
        self._status = StateProgress.WAITING
        self.data = info_request
        self.imgs = self.data.extact_imgs_request()
        self.length = len(self.imgs)
        self._progress = 0

    def download(self):
        self.status = StateProgress.DOWNLOADING
        for img in self.imgs:
            img.download()
            self.progress = self.progress + 1
        self.status = StateProgress.SUCCESS

    @GObject.Property(type=object)
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.notify('status')

    @GObject.Property(type=int)
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.notify('progress')


class DownloadManager(GObject.GObject):

    def __init__(self):
        super().__init__()
        self._downloading = False
        self.queue: Gio.ListStore = Gio.ListStore()
        self.end_queue: Gio.ListStore = Gio.ListStore()

    def append(self, info_request: InfoRequest):
        self.queue.append(DownloadItemStates(info_request))

    @GObject.Property(type=bool, default=False)
    def downloading(self):
        return self._downloading

    @downloading.setter
    def downloading(self, value: bool):
        self._downloading = value
        self.notify('downloading')

    def downloads(self):
        if self.queue.get_n_items() < 1:
            self.downloading = False
            return

        if self.downloading:
            return

        self.downloading = True
        self.queue.get_item(0).download()
        self.end_queue.append(self.queue.get_item(0))
        self.queue.remove(0)
        self.downloading = False
        self.downloads()
