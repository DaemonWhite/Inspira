from gi.repository import GLib
from .unique_list import UniqueList
import json
import os

def get_tags_api_path():
    return os.path.join(GLib.get_user_config_dir(), "inspira", "tags.json")


class TagsStorage(object):
    def __init__(self):
        self.__path = get_tags_api_path()
        self.__tags = {
            "nsfw": UniqueList(),
            "sfw": UniqueList()
        }

    def get_tags(self) -> dict:
        self.__tags.copy()

    def load_tags(self):
        if not os.path.isfile(self.__path):
            return
        try:
            with open(self.__path, "r", encoding="utf-8") as f:
                tags = json.load(f)
                self.__tags["nsfw"].extend(tags["nsfw"])
                self.__tags["sfw"].extend(tags["sfw"])
        except:
            print("File missing or corrupt")

    def save_tags(self):
        with open(self.__path, "w", encoding="utf-8") as f:
            json.dump(self.__tags, f, ensure_ascii=False, indent=4)
