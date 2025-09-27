from gi.repository import GLib

from .interfaceAPI import InterfaceAPI


class Manager(object):
    def __init__(self):
        self.plugins: Dict[str, Dict[str, object]] = {}

    def register(self, plugin: InterfaceAPI, active: bool = False):
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
        count = InterfaceAPI.clamp(count, plugin.randomCapability)
        return plugin.random(count, nsfw, tags)

    def download(self, plugins_name: str, data) -> bytes:
        return self.plugins[plugins_name]["instance"].download(data)
