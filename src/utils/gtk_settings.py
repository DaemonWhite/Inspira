from gi.repository import Gio


class InspiraSettings(Gio.Settings):

    def __init__(self,):
        super().__init__("fr.daemonwhite.Inspira")

    @property
    def auto_save_tags(self) -> bool:
        return self.get_boolean("auto-save-tags")

    @auto_save_tags.setter
    def auto_save_tags(self, enable: bool):
        self.set_boolean("auto-save-tags")

    @property
    def global_nsfw(self) -> bool:
        return self.get_boolean("global-nsfw")

    @global_nsfw.setter
    def global_nsfw(self, enable: bool):
        self.set_boolean("global-nsfw")

    @property
    def timeout_download(self) -> int:
        return self.get_int("timeout-download")

    @timeout_download.setter
    def timeout_download(self, value: bool):
        self.set_int("timeout-download", value)
