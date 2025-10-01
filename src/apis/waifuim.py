from ..core.ApiInterface import ApiInterface
from ..core.capability import EndPointCapability, TagCapability


class WaifuIm(ApiInterface):
    def __init__(self):
        super()
        self._name = "Waifu.im"
        self._urlAPI = "https://api.waifu.im/"

        tag = TagCapability(
            present=True,
            know=[
                "maid",
                "waifu",
                "marin-kitagawa",
                "mori-calliope",
                "raiden-shogun",
                "oppai",
                "selfies",
                "uniform",
                "kamisato-ayaka"
            ],
            know_nsfw=[
                "ass",
                "hentai",
                "milf",
                "oral",
                "paizuri",
                "ecchi",
                "ero"
            ]
        )

        self.randomCapability = EndPointCapability(
            present=True,
            nsfw=True,
            tag=tag,
            limit_min=1,
            limit_max=30
        )
        self.searchCapability = EndPointCapability(
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

        if len(tags) > 0:
            params['included_tags'] = tags

        data, error = self._safe_request(
            url,
            params,
            self.randomCapability.timeout,
            True
        )

        return self._make_response(tags, params, data, error)

    def download(self, content):
        print(content)
        return self._download_bytes(content["data"]['images'][0]['url'])
