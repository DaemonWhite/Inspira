from .interfaceAPI import InterfaceAPI
from .capability import Capability
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
            tags=True,
            limit_min=1,
            limit_max=20
        )

    def search(self, count: int, nsfw: bool, tags: list):
        pass

    def random(self, count: int, nsfw: bool, tags: list):
        url = self._urlAPI + "/random/image"

        params = {}
        params["nsfw"] = InterfaceAPI.str_bool(nsfw)
        params["count"] = count

        return self._download_text(
            url,
            params,
            self.randomCapability.timeout
        )


    def download(self, content):
        data = json.loads(content)

        url = "https://nekos.moe/image/" + data["images"][0]['id']
        return self._download_bytes(url)


