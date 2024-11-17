import os
from dataclasses import asdict
from functools import cache, cached_property

from utils import JSONFile, Log

from utils_future.StringX import StringX

log = Log("Storable")


class Storable(object):
    @classmethod
    @cache
    def get_data_dir(cls):
        data_dir = os.path.join(
            "data", StringX(cls.__name__).snake_case + "s"
        )
        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    @cached_property
    def json_file(self):
        return JSONFile(os.path.join(self.get_data_dir(), f"{self.id}.json"))

    def store(self):
        if self.json_file.exists:
            return
        self.json_file.write(asdict(self))
        log.info(f"Wrote {self.json_file.path}")

    @classmethod
    def list_all(Cls) -> list["Storable"]:
        data_dir = Cls.get_data_dir()
        cls_list = []
        for file in os.listdir(data_dir):
            if file.endswith(".json"):
                d = JSONFile(os.path.join(data_dir, file)).read()
                cls_list.append(Cls(**d))
        return cls_list
