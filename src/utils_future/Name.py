import os
from functools import cache

from utils import JSONFile, Log

log = Log("Name")


class Name:

    NAME_IDX_FILE = JSONFile(
        os.path.join("src", "utils_future", "data", "name_idx.human.json")
    )

    @staticmethod
    @cache
    def name_idx():
        idx_raw = Name.NAME_IDX_FILE.read()
        idx = {}
        for k, v_list in idx_raw.items():
            for v in v_list:
                idx[v] = k
        return idx

    @staticmethod
    @cache
    def get_norm_name(s):
        return Name.name_idx().get(s, s).replace(".", "").strip()
