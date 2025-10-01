from ..core.ApiInterface import ApiInterface
from ..core.capability import EndPointCapability, TagCapability


class NekoMoe(ApiInterface):
    def __init__(self):
        super()
        self._name = "NekoMoe"
        self._urlAPI = "https://nekos.moe/api/v1/"

        self.randomCapability = EndPointCapability(
            present=True,
            nsfw=True,
            limit_min=1,
            limit_max=100
        )
        self.searchCapability = EndPointCapability(
            present=True,
            nsfw=True,
            tag=TagCapability(present=True),
            limit_min=1,
            limit_max=20
        )

    def search(self, count: int, nsfw: bool, tags: list):
        pass

    def random(self, count: int, nsfw: bool, tags: list):
        url = self._urlAPI + "/random/image"

        params = {}
        params["nsfw"] = ApiInterface.str_bool(nsfw)
        params["count"] = count

        data, error = self._safe_request(
            url,
            params,
            self.randomCapability.timeout,
            True
        )

        return self._make_response(tags, params, data, error)


    def download(self, content):
        url = "https://nekos.moe/image/" + content["data"]["images"][0]['id']
        return self._download_bytes(url)


