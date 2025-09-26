from .capability import Capability

class InterfaceAPI:
    def __init__(self):
        self._name: str = "Unknow"
        self._urlAPI: str = "https://nekos.moe/api/v1/"
        self.randomCapability = Capability()
        self.searchCapability = Capability()

    @property
    def name(self) -> str:
        return self._name

    def search(self, tags):
        raise NotImplementedError("Search must be overridden")

    def random(self, tags):
        raise NotImplementedError("Search must be overridden")
