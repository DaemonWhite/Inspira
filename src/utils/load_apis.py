import pkgutil
import importlib
import os
import json


import config

from gi.repository import GLib

from ..core.ApiInterface import ApiInterface


def load_apis(full_path: str, package:str):
    plugins = []
    for name, module_name, finder in pkgutil.iter_modules(["/app/share/inspira/inspira/apis"]):
        print(f"Module find : {name}, Package : {module_name}")

        module = importlib.import_module(f".apis.{module_name}", package=package)
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, ApiInterface) and obj is not ApiInterface:
                plugins.append(obj())
    return plugins


def get_conf_api_path():
    return os.path.join(GLib.get_user_config_dir(), "inspira", "api.json")


def creat_config_path():
    print("")
    config_path = GLib.get_user_config_dir()
    if not os.path.exists(config_path):
        print("Error: xdg config")
        return 2

    config_path = os.path.join(config_path, "inspira")
    if not os.path.exists(config_path):
        print("path not exist")
        os.mkdir(config_path)
        return creat_config_path()

    return 0


def load_config_api():
    api_path = get_conf_api_path()

    if not os.path.isfile(api_path):
        return {}
    try:
        with open(api_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print("File missing or corrupt")
        return {}


def save_config_api(list_plugins):
    api_path = get_conf_api_path()
    apis: dict = {}
    for api in list_plugins:
        apis[api['name']] = api['active']

    with open(api_path, "w", encoding="utf-8") as f:
        json.dump(apis, f, ensure_ascii=False, indent=4)
