from easydict import EasyDict as edict
from pathlib import Path

from typing import Union


class Config:
    def __init__(self, path: Union[str, Path]):
        path = str(path)
        if path.endswith("yaml"):
            import yaml

            load = yaml.safe_load
        elif path.endswith("json"):
            import json

            load = json.load
        elif path.endswith("jsonc"):
            from jsoncomment import JsonC

            load = JsonC().load

        with open(path, "r") as f:
            config = load(f)
        config = edict(config)

        for k, v in config.items():
            setattr(self, k, v)
