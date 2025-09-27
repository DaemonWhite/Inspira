import pkgutil
import importlib
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
