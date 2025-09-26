import requests
from typing import Optional

from .capability import Capability

class InterfaceAPI:
    def __init__(self):
        self._name: str = "Unknown"
        self._urlAPI: str = "https://nekos.moe/api/v1/"
        self.randomCapability = Capability()
        self.searchCapability = Capability()

    @property
    def name(self) -> str:
        return self._name

    def search(self, tags):
        raise NotImplementedError("Search must be overridden")

    def random(self, tags):
        raise NotImplementedError("random must be overridden")

    def download(self, content) -> Optional[bytes]:
        raise NotImplementedError("random must be overridden")

    def _download_text(self, url: str, timeout: int) -> Optional[str]:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.text
        return None

    def _download_bytes(self, url:str, timeout: int=10) -> Optional[bytes]:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.content
        return None
