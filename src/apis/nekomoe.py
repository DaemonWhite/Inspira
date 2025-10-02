# nekomoe.py
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

from ..core.ApiInterface import ApiInterface
from ..core.capability import EndPointCapability, TagCapability
from ..core.imgData import ImgData
from ..core.infoRequest import InfoRequest


class NekoMoe(ApiInterface):
    def __init__(self):
        super()
        self._name = "NekoMoe"
        self._urlAPI = "https://nekos.moe/api/v1/"
        self._downloadUrl = "https://nekos.moe/image/"

        self.randomCapability = EndPointCapability(
            present=True,
            nsfw=True,
            limit_min=1,
            limit_max=100
        )
        self.searchCapability = EndPointCapability(
            present=True,
            nsfw=True,
            tag=TagCapability(present=True),
            limit_min=1,
            limit_max=20
        )

    def search(self, count: int, nsfw: bool, tags: list) -> InfoRequest:
        pass

    def random(self, count: int, nsfw: bool, tags: list) -> InfoRequest:
        url = self._urlAPI + "/random/image"

        params = {}
        params["nsfw"] = ApiInterface.str_bool(nsfw)
        params["count"] = count

        data, error = self._safe_request(
            url,
            params,
            self.randomCapability.timeout,
            True
        )

        return self._make_response(tags, params, nsfw, data, error)

    def _img_format(self, info_request: InfoRequest) -> ImgData:
        imgs: list[ImgData] = []
        for value in info_request.data['images']:
            img = ImgData(
                info_request=info_request,
                img_tags=value['tags'],
                img_url=f"{self._downloadUrl}/{value['id']}",
                autor=value['artist'],
                timeout=10
            )
            imgs.append(img)

        return imgs


