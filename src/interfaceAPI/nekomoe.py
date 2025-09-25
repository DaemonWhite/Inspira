from .interfaceAPI import InterfaceAPI
import requests

class NekoMoe(InterfaceAPI):
    def __init__(self):
        super()
        self._name = "NekoMoe"
        self._urlAPI = "https://nekos.moe/api/v1/"
        self._nsfw = True
        self._supportRandomFilter = False

    def search(self, tags):
        pass

    def random(self, tags):
        url = self._urlAPI + f"/random/image?nsfw={self.nsfw}"

        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
        else:
            return None
