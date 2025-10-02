# waifuim.py
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
from ..core.infoRequest import InfoRequest
from ..core.imgData import ImgData


class WaifuIm(ApiInterface):
    def __init__(self):
        super()
        self._name = "Waifu.im"
        self._urlAPI = "https://api.waifu.im/"

        tag = TagCapability(
            present=True,
            know=[
                "maid",
                "waifu",
                "marin-kitagawa",
                "mori-calliope",
                "raiden-shogun",
                "oppai",
                "selfies",
                "uniform",
                "kamisato-ayaka"
            ],
            know_nsfw=[
                "ass",
                "hentai",
                "milf",
                "oral",
                "paizuri",
                "ecchi",
                "ero"
            ]
        )

        self.randomCapability = EndPointCapability(
            present=True,
            nsfw=True,
            tag=tag,
            limit_min=1,
            limit_max=30
        )
        self.searchCapability = EndPointCapability(
            present=False,
            nsfw=True,
            limit_min=1,
            limit_max=30
        )

    def search(self, count: int, nsfw: bool, tags: list) -> InfoRequest:
        pass

    def random(self, count: int, nsfw: bool, tags: list) -> InfoRequest:
        count = self.clamp(count, self.randomCapability)

        url = self._urlAPI + "search"

        params = {}
        params["is_nsfw"] = nsfw

        if count > 1:
            params['limit'] = count

        if len(tags) > 0:
            params['included_tags'] = tags

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
            autor = value["artist"]["name"] if value.get("artist") else None
            img = ImgData(
                info_request=info_request,
                img_tags=[item["name"] for item in value["tags"]],
                img_url=value['url'],
                autor=autor,
                timeout=10
            )
            imgs.append(img)

        return imgs
