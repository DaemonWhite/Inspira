import requests
from typing import Optional

from .capability import EndPointCapability
from .infoRequest import InfoRequest
from .imgData import ImgData


class ApiInterface:
    def __init__(self):
        self._name: str = "Unknown"
        self._urlAPI: str = "https://example.com/api/v1/"
        self.randomCapability = EndPointCapability()
        self.searchCapability = EndPointCapability()

    @property
    def name(self) -> str:
        return self._name

    def search(
            self,
            count: int,
            nsfw: bool,
            tags_include: list,
            tags_exlclude: list,
            sort: str,
            skip: int) -> InfoRequest:
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
    def clamp(count: int, capability: EndPointCapability) -> int:
        if count < capability.limit_min:
            count = capability.limit_min
        elif count > capability.limit_max:
            count = capability.limit_max
        return count

    def random(self, count: int, nsfw: bool, tags: list[str]) -> InfoRequest:
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
                nsfw: bool,
                data: dict | None,
                error: str | None = None
            ) -> InfoRequest:
        return InfoRequest(
            api_name=self._name,
            search_tags=tags,
            request=params,
            nsfw=nsfw,
            success=error is None,
            error=error,
            data=data,
            handler_extact_request=self._img_format
        )

    def _img_format(self, info_request: InfoRequest) -> ImgData:
        raise NotImplementedError("random must be overridden")

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
                r = requests.post(url, json=params, timeout=timeout)
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
