import requests
from typing import Optional

from .capability import EndPointCapability


class ApiInterface:
    def __init__(self):
        self._name: str = "Unknown"
        self._urlAPI: str = "https://nekos.moe/api/v1/"
        self.randomCapability = EndPointCapability()
        self.searchCapability = EndPointCapability()

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
    def clamp(count: int, capability: EndPointCapability):
        if count < capability.limit_min:
            count = capability.limit_min
        elif count > capability.limit_max:
            count = capability.limit_max
        return count

    def random(self, count: int, nsfw: bool, tags: list[str]):
        raise NotImplementedError("random must be overridden")

    def download(self, content) -> Optional[bytes]:
        raise NotImplementedError("random must be overridden")

    def get_know_tags(self, nsfw=False):
        tags = self.randomCapability.tag.know
        if nsfw:
            tags.append(self.randomCapability.tag.know_nsfw)
        return tags

    def _make_response(
                self,
                tags: list,
                params: dict,
                data: dict | None,
                error: str |
                None = None
            ) -> dict:
        return {
            "name": self._name,
            "tags": tags,
            "request": params,
            "success": error is None,
            "error": error,
            "data": data if data else {}
        }

    def _safe_request(
                self,
                url: str,
                params: dict,
                timeout: int = 10,
                is_get: bool = True
            ) -> tuple[dict | None, str | None]:
        try:
            if is_get:
                r = requests.get(url, params=params, timeout=timeout)
            else:
                r = requests.post(url, params=params, timeout=timeout)

            if r.status_code == 200:
                return r.json(), None
            else:
                return None, f"HTTP {r.status_code}: {r.text}"
        except requests.Timeout:
            return None, "Request timed out"
        except requests.RequestException as e:
            return None, f"Request failed: {str(e)}"

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
