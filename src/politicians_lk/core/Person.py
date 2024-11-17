import os
from dataclasses import dataclass
from datetime import datetime
from functools import cache, cached_property

from utils import JSONFile, Log

log = Log("Person")


@dataclass
class Person(object):
    name_list: list[str]
    dob: datetime
    dod: datetime
    gender: str

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def from_full_name_fuzzy(cls, full_name: str) -> "Person":
        full_name = full_name.replace(".", "").replace("\n", "").strip()
        name_list = [name for name in full_name.split(" ") if name.strip()]

        person = cls(
            name_list,
            gender=None,
            dob=None,
            dod=None,
        )
        person.store()
        return person

    @cached_property
    def id(self):
        return "-".join(self.name_list)

    @cache
    def to_dict(self):
        return dict(
            name_list=self.name_list,
            gender=self.gender,
            dob=self.dob,
            dod=self.dod,
        )

    def from_dict(cls, d):
        return cls(
            name_list=d["name_list"],
            gender=d["gender"],
            dob=d["dob"],
            dod=d["dod"],
        )

    @classmethod
    @cache
    def get_data_dir(cls):
        data_dir = os.path.join("data", cls.__name__.lower() + "s")
        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    @cached_property
    def json_file(self):
        return JSONFile(os.path.join(self.get_data_dir(), f"{self.id}.json"))

    def store(self):
        if self.json_file.exists:
            return
        self.json_file.write(self.to_dict())
        log.info(f"Wrote {self.json_file.path}")
