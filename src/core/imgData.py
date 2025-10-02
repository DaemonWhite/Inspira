# imgData.py
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

import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .infoRequest import InfoReques


class ImgData(object):
    def __init__(
                self,
                info_request: "InfoRequest",
                img_tags: list[str],
                img_url: str,
                autor: str,
                timeout: int
            ):
        self._info_request: "InfoRequest" = info_request
        self._img_tags: list[str] = img_tags
        self._autor: str = autor
        self._img_url: str = img_url
        self._timeout: int = timeout

        self._success: bool = False
        self._error: list[str] = []
        self._img: bytes = None

    @property
    def autor(self) -> str:
        return self._autor

    @property
    def api_name(self) -> str:
        return self._info_request.api_name

    @property
    def search_tags(self) -> list[str]:
        return self._info_request.search_tags

    @property
    def success(self) -> bool:
        return self._success

    @property
    def error(self) -> list[str]:
        return self._error

    @property
    def img_tags(self) -> "InfoReques":
        return self._img_tags

    @property
    def img(self) -> bytes:
        return self._img

    @property
    def url(self) -> str:
        return self._img_url

    def __str__(self):
        return f"ImgData(\n\t\
success={self.success},\n\t\
img_url={self._img_url},\n\t\
timeout={self._timeout},\n\t\
error={self._error},\n\t\
img_tags={self._img_tags},\n\t\
autor={self._autor},\n\t\
info_request={self._info_request},\n\
)"

    def __repr__(self):
        return f"ImgData(\
success={self.success},\
 img_url={self._img_url},\
 timeout={self._timeout},\
 error={self._error},\
 img_tags={self._img_tags},\
 autor={self._autor},\
 info_request={self._info_request},\
 img={self._img})"

    def download(self) -> bytes | None:
        self._success = False
        try:
            r = requests.get(self._img_url, timeout=self._timeout)

            if r.status_code == 200:
                self._success = True
                self._img = r.content or None
                return self._img
            else:
                self._error.append(f"HTTP {r.status_code}: {r.text}")
                return None
        except requests.Timeout:
            self._error.append("Request timed out")
            return None
        except requests.RequestException as e:
            self._error.append(f"Request failed: {str(e)}")
            return None
