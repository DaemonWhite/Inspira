from gi.repository import GLib

from .ApiInterface import ApiInterface
from ..utils import add_without_duplicate


class Manager(object):
    def __init__(self):
        self.plugins: dict[str, dict[str, object]] = {}

    def register(self, plugin: ApiInterface, active: bool = False):
        self.plugins[plugin.name] = {
            "instance": plugin,
            "active": True
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
                    "random": data["instance"].randomCapability.present,
                    "search": data["instance"].searchCapability.present,
                }
            }
            for n, data in self.plugins.items()
        ]

    def random(self, plugins_name: str, count: int=-1, nsfw: bool=False, tags: list[str]= []):
        plugin = self.plugins[plugins_name]["instance"]
        count = ApiInterface.clamp(count, plugin.randomCapability)
        return plugin.random(count, nsfw, tags)

    def download(self, plugins_name: str, data) -> bytes:
        return self.plugins[plugins_name]["instance"].download(data)

    def get_all_tags(self) -> list:
        tags: list = []
        for name, plugin in self.plugins.items():
            know_tags = plugin['instance'].get_know_tags()
            if len(know_tags) <= 0:
                continue

            for tag in know_tags:
                add_without_duplicate(tags, tag)
        return tags
