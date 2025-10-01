# infoRequest.py
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

from .imgData import ImgData


class InfoRequest(object):
    def __init__(
                self, api_name: str,
                search_tags: list[str],
                request: dict,
                success: bool,
                error: list[str],
                data: dict,
                handler_extact_request
            ):
        self._name: str = api_name
        self._search_tags: list[str] = search_tags
        self._request: dict = request
        self._success: bool = success
        self._error: list[str] = error
        self._data: dict = data
        self._handler_extact_request = handler_extact_request

    @property
    def api_name(self) -> str:
        return self._name

    @property
    def data(self) -> dict:
        return self._data

    @property
    def search_tags(self) -> list[str]:
        return self._search_tags

    @property
    def request(self) -> dict:
        return self._request

    @property
    def success(self) -> bool:
        return self._success

    @property
    def error(self) -> list[str]:
        return self._error

    def extact_imgs_request(self) -> list[ImgData]:
        return self._handler_extact_request(self)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"InfoRequest(api_name={self.api_name},\
 search_tags={self.search_tags},\
 request={self.request},\
 success={self._success},\
 error={self.error},\
 data={self._data})"
