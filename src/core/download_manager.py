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
from enum import Enum

from .imgData import ImgData
from .infoRequest import InfoRequest


class DownloadState(Enum):
    WAIT = 0
    DOWNLOAD = 1
    FINISH = 2


class DownloadItemStates(GObject.GObject):
    data = GObject.Property(type=object)
    state = GObject.Property(type=object)
    lenght = GObject.Property(type=int)
    advanced = GObject.Property(type=int)
    imgs =  GObject.Property(type=object)

    def __init__(self, info_request: InfoRequest):
        super().__init__()
        self.state = DownloadState.WAIT
        self.data = info_request
        self.imgs = self.data.extact_imgs_request()
        self.lenght = len(self.imgs)
        self.advanced = 0

    def download(self):
        self.state = DownloadState.DOWNLOAD
        self.imgs[0].download()
        self.state = DownloadState.FINISH
        print("end")


class DownloadManager():

    def __init__(self):
        super().__init__()
        self.downloaded = False
        self.queue: Gio.ListStore = Gio.ListStore()
        self.end_queue: Gio.ListStore = Gio.ListStore()

    def append(self, info_request: InfoRequest):
        self.queue.append(DownloadItemStates(info_request))

    def downloads(self):
        if self.queue.get_n_items() < 1:
            self.downloaded = False
            return

        if self.downloaded:
            return

        self.downloaded = True
        self.queue.get_item(0).download()
        self.end_queue = self.queue.get_item(0)
        self.queue.remove(0)
        self.downloads()
