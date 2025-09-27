import requests
from typing import Optional

from .capability import Capability


## TODO Ajouter Info data
class ApiInterface:
    def __init__(self):
        self._name: str = "Unknown"
        self._urlAPI: str = "https://nekos.moe/api/v1/"
        self.randomCapability = Capability()
        self.searchCapability = Capability()

    @property
    def name(self) -> str:
        return self._name

    def search(self, count: int, nsfw: bool, tags: list):
        raise NotImplementedError("Search must be overridden")

    @staticmethod
    def str_bool(boolean: bool) -> str:
        return f"{boolean}".lower()

    @staticmethod
    def int_bool(boolean: bool) -> int:
        if boolean:
            return 1
        return 0

    @staticmethod
    def clamp(count: int, capability: Capability):
        if count < capability.limit_min:
            count = capability.limit_min
        elif count > capability.limit_max:
            count = capability.limit_max
        return count

    def random(self, count: int, nsfw: bool, tags: list[str]):
        raise NotImplementedError("random must be overridden")

    def download(self, content) -> Optional[bytes]:
        raise NotImplementedError("random must be overridden")

    def _download_text(
                self,
                url: str,
                params: dict = {},
                timeout: int = 10,
                is_get: bool = True,
            ) -> Optional[str]:
        r = None

        if is_get:
            r = requests.get(url, params=params, timeout=timeout)
        else:
            r = requests.post(url, params=params, timeout=timeout)

        if r.status_code == 200:
            return r.text
        return None

    def _download_bytes(
                self,
                url: str,
                params: dict = {},
                timeout: int = 10,
                is_get: bool = True,
            ) -> Optional[bytes]:
        r = None

        if is_get:
            r = requests.get(url, params=params, timeout=timeout)
        else:
            r = requests.post(url, params=params, timeout=timeout)

        if r.status_code == 200:
            return r.content
        return None
