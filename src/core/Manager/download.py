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
import queue
import threading

from gi.repository import Gio, GObject, GLib

from ...utils.state_progress import StateProgress

from ..Api import ImgData, InfoRequest


class DownloadItemStates(GObject.GObject):
    data = GObject.Property(type=object)
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
        GLib.idle_add(self._update_status, StateProgress.DOWNLOADING)
        for img in self.imgs:
            img.download()
            GLib.idle_add(self._update_progress, self._progress + 1)

        GLib.idle_add(self._update_status, StateProgress.SUCCESS)

    def _update_status(self, new_status):
        self.status = new_status
        return False

    def _update_progress(self, new_progress):
        self.progress = new_progress
        return False

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

    __gsignals__ = {
        'add-item': (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    def __init__(self):
        super().__init__()
        self._downloading = False

        self.end_queue: Gio.ListStore = Gio.ListStore()

        self._work_queue = queue.Queue()

        self._stop_event = threading.Event()

        self._worker = threading.Thread(
            target=self._worker_thread,
            name="DownloadWorker"
        )

        self._worker.start()

    def append(self, info_request: InfoRequest):
        item = DownloadItemStates(info_request)

        self._work_queue.put(item)

        GLib.idle_add(self._emit_add_item, item)

    def _emit_add_item(self, item):
        self.emit('add-item', item)
        return False

    @GObject.Property(type=bool, default=False)
    def downloading(self):
        return self._downloading

    @downloading.setter
    def downloading(self, value: bool):
        self._downloading = value
        self.notify('downloading')

    def _worker_thread(self):
        while not self._stop_event.is_set():
            try:
                item = self._work_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if item is None:
                break

            GLib.idle_add(self._set_downloading, True)

            try:
                item.download()
                GLib.idle_add(self._on_download_complete, item)
            except Exception as e:
                print(f"Error download: {e}")
                GLib.idle_add(self._on_download_error, item, str(e))
            finally:
                self._work_queue.task_done()

        print("Worker thread success end proccess")

    def shutdown(self):
        print("Down DownloadManager...")
        self._stop_event.set()
        self._work_queue.put(None)
        self._worker.join(timeout=5.0)

        if self._worker.is_alive():
            print("Warning: Donwload manager butal force down")
        else:
            print("DownloadManager success down")

    def _set_downloading(self, value):
        self.downloading = value
        return False  # Ne pas répéter l'appel

    def _on_download_complete(self, item):

        self.end_queue.append(item)

        if self._work_queue.empty():
            self.downloading = False

        return False

    def _on_download_error(self, item, error):
        print(f"Error Download: {error}")

        item.status = StateProgress.ERROR

        self.end_queue.append(item)

        if self._work_queue.empty():
            self.downloading = False

        return False

    def cancel_all(self):
        while not self._work_queue.empty():
            try:
                self._work_queue.get_nowait()
                self._work_queue.task_done()
            except queue.Empty:
                break

        self.downloading = False
