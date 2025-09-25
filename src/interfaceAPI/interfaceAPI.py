class InterfaceAPI:
    def __init__(self):
        self._name: str = "Unknow"
        self._urlAPI: str = "https://nekos.moe/api/v1/"
        self._supportRandomFilter: bool = False
        self._nsfw: bool = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def supportRandomFilter(self) -> bool:
        return self._supportRandomFilter

    @property
    def nsfw(self) -> bool:
        return self._nsfw

    def supportRandomFilter(self) -> bool:
        return self.__supportRandomFilter

    def search(self, tags):
        raise NotImplementedError("Search must be overridden")

    def random(self, tags):
        raise NotImplementedError("Search must be overridden")


