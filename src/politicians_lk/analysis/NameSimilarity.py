import os

from fuzzywuzzy import fuzz
from utils import JSONFile, Log

from politicians_lk.core import Politician

log = Log("NameSimilarity")


class NameSimilarity:
    @staticmethod
    def get_dir_path():
        dir_path = os.path.join("data", "analysis", "name_similarity")
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    DIR_PATH = get_dir_path()

    def get_similarity_info_list(self, min_ratio, max_ratio):
        politician_list = Politician.list_all()
        n = len(politician_list)

        info_list = []
        for i1 in range(n):
            full_name1 = politician_list[i1].full_name

            for i2 in range(i1 + 1, n):
                full_name2 = politician_list[i2].full_name

                ratio = fuzz.ratio(full_name1, full_name2)
                if min_ratio < ratio <= max_ratio:
                    info = dict(
                        full_name1=full_name1,
                        full_name2=full_name2,
                        ratio=ratio,
                    )
                    info_list.append(info)
        log.debug(f"Found {len(info_list)} infos from {n} politicians")
        return info_list

    def get_idx(self, min_ratio, max_ratio):
        info_list = self.get_similarity_info_list(min_ratio, max_ratio)
        idx = {}
        for info in info_list:
            full_name1 = info["full_name1"]
            full_name2 = info["full_name2"]

            if full_name1 not in idx:
                idx[full_name1] = [full_name1]

            idx[full_name1].append(full_name2)

        file_path = os.path.join(
            self.DIR_PATH, f"{min_ratio:03d}-{max_ratio:03d}.json"
        )
        JSONFile(file_path).write(idx)
        log.info(f"Wrote {file_path}")
        return idx


if __name__ == "__main__":
    for min_ratio, max_ratio in [
        (80, 81),
        (81, 82),
        (82, 83),
        (83, 84),
        (84, 85),
        (85, 100),
    ]:
        NameSimilarity().get_idx(min_ratio, max_ratio)
