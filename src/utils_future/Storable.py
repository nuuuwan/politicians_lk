import os
from dataclasses import asdict
from functools import cache, cached_property

from utils import JSONFile, Log

from utils_future.StringX import StringX
from utils_future.TSVFile import TSVFile

log = Log("Storable")


class Storable(object):
    @classmethod
    @cache
    def get_id(Class):
        return StringX(Class.__name__).snake_case + "s"

    @classmethod
    @cache
    def get_data_dir(Class):
        data_dir = os.path.join("data", "core", Class.get_id())
        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    @cached_property
    def json_file(self):
        return JSONFile(os.path.join(self.get_data_dir(), f"{self.id}.json"))

    def store(self):
        if self.json_file.exists:
            return
        self.json_file.write(asdict(self))

    @classmethod
    def list_all(Class) -> list["Storable"]:
        data_dir = Class.get_data_dir()
        Class_list = []
        for file in os.listdir(data_dir):
            if file.endswith(".json"):
                d = JSONFile(os.path.join(data_dir, file)).read()
                Class_list.append(Class(**d))
        return Class_list

    @cached_property
    def custom_d(self):
        return {}

    @classmethod
    def to_tsv(Class):
        Class.get_data_dir()
        tsv_file_path = os.path.join("data", "core", f"{Class.get_id()}.tsv")

        d_list = [asdict(ins) | ins.custom_d for ins in Class.list_all()]
        TSVFile(tsv_file_path).write(d_list)
        log.info(f'Wrote {len(d_list)} rows to "{tsv_file_path}"')
        return tsv_file_path
