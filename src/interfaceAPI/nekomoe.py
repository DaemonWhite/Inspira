from .interfaceAPI import InterfaceAPI
from .capability import Capability
import requests
import json

class NekoMoe(InterfaceAPI):
    def __init__(self):
        super()
        self._name = "NekoMoe"
        self._urlAPI = "https://nekos.moe/api/v1/"

        self.randomCapability = Capability(
            present=True,
            nsfw=True,
            limit_min=1,
            limit_max=100
        )
        self.searchCapability = Capability(
            present=True,
            nsfw=True,
            limit_min=1,
            limit_max=20
        )

    def search(self, tags):
        pass

    def random(self, tags):
        url = self._urlAPI + f"/random/image?nsfw={self.randomCapability.nsfw}"

        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
        else:
            return None

    def downloads(self, content):
        data = json.loads(content)
        url = "https://nekos.moe/image/" + data["images"][0]['id']
        print(url)
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.content
        else:
            return None
