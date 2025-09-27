from .interfaceAPI import InterfaceAPI
from .capability import Capability
import json


class WaifuIm(InterfaceAPI):
    def __init__(self):
        super()
        self._name = "Waifu.im"
        self._urlAPI = "https://api.waifu.im/"
        knowTag = [
            "maid",
            "waifu",
            "marin-kitagawa",
            "mori-calliope",
            "raiden-shogun",
            "oppai",
            "selfies",
            "uniform",
            "kamisato-ayaka"
        ]
        self.randomCapability = Capability(
            present=True,
            nsfw=True,
            know_tags=knowTag,
            tags=True,
            limit_min=1,
            limit_max=30
        )
        self.searchCapability = Capability(
            present=False,
            nsfw=True,
            limit_min=1,
            limit_max=30
        )

    def search(self, count: int, nsfw: bool, tags: list):
        pass

    def random(self, count: int, nsfw: bool, tags: list):
        count = self.clamp(count, self.randomCapability)

        url = self._urlAPI + "search"

        params = {}
        params["is_nsfw"] = nsfw

        if count > 1:
            params['limit'] = count
        return self._download_text(
            url,
            params,
            self.randomCapability.timeout
        )

    def download(self, content):
        data = json.loads(content)
        return self._download_bytes(data['images'][0]['url'])
