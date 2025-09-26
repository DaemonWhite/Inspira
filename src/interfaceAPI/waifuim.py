from .interfaceAPI import InterfaceAPI
from .capability import Capability
import requests
import json

class WaifuIm(InterfaceAPI):
    def __init__(self):
        super()
        self._name = "Waifu.im"
        self._urlAPI = "https://api.waifu.im/"
        knowTag = ["maid",
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
            limit_min=1,
            limit_max=100
        )
        self.searchCapability = Capability(
            present=False,
            nsfw=True,
            limit_min=1,
            limit_max=30
        )

    def search(self, tags):
        pass

    def random(self, tags):
        url = self._urlAPI + f"/search?is_nsfw={self.randomCapability.nsfw}"
        return self._download_text(url, self.randomCapability.timeout)

    def download(self, content):
        data = json.loads(content)
        return self._download_bytes(data['images'][0]['url'])
