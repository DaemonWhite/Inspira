# manager.py
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

from .infoRequest import InfoRequest

from .ApiInterface import ApiInterface
from ..utils import add_without_duplicate


class Manager(object):
    def __init__(self):
        self.plugins: dict[str, dict[str, object]] = {}

    def register(self, plugin: ApiInterface, active: bool = False):
        self.plugins[plugin.name] = {
            "instance": plugin,
            "active": active
        }

    def enable(self, name: str):
        if name in self.plugins:
            self.plugins[name]["active"] = True

    def disable(self, name: str):
        if name in self.plugins:
            self.plugins[name]["active"] = False

    def list_plugins(self) -> list[dict]:
        return [
            {
                "name": n,
                "active": data["active"],
                "capabilities": {
                    "random": data["instance"].randomCapability,
                    "search": data["instance"].searchCapability,
                }
            }
            for n, data in self.plugins.items()
        ]

    def random(
            self,
            plugins_name: str,
            count: int = -1,
            nsfw: bool = False,
            tags: list[str] = []
        ) -> InfoRequest:
        plugin = self.plugins[plugins_name]["instance"]
        count = ApiInterface.clamp(count, plugin.randomCapability)
        return plugin.random(count, nsfw, tags)

    def get_all_tags(self) -> list:
        tags: list = []
        for name, plugin in self.plugins.items():
            know_tags = plugin['instance'].get_know_tags()
            if len(know_tags) <= 0:
                continue

            for tag in know_tags:
                add_without_duplicate(tags, tag)
        return tags
