import os
import time

import requests
import wikipedia
from fuzzywuzzy import fuzz
from utils import JSONFile, Log

from politicians_lk.core import Politician

log = Log("NameSimilarity")


class NameSimilarity:
    MIN_FUZZ_RATIO = 92

    def run(self):
        politician_list = Politician.list_all()
        n = len(politician_list)
        sim_group = {}
        for i1 in range(n):
            p1 = politician_list[i1]
            full_name1 = p1.full_name
            for i2 in range(i1 + 1, n):
                p2 = politician_list[i2]
                full_name2 = p2.full_name
                ratio = fuzz.ratio(full_name1, full_name2)
                if ratio >= NameSimilarity.MIN_FUZZ_RATIO:
                    log.debug(f'{ratio}: "{full_name1}" & "{full_name2}"')

                    if full_name1 not in sim_group:
                        sim_group[full_name1] = [full_name1]
                    sim_group[full_name1].append(full_name2)

        idx = {}
        for k, v in sim_group.items():
            result_to_count = {}
            for name in v:

                timeout = 1
                while True:
                    try:
                        results = wikipedia.search(name, results=1)
                        break
                    except requests.exceptions.ConnectTimeout as e:
                        log.error(f"[{timeout}s] {e}")
                        time.sleep(timeout)
                        timeout *= 2

                for result in results:
                    if (
                        fuzz.ratio(result, name)
                        >= NameSimilarity.MIN_FUZZ_RATIO
                    ):
                        if result not in result_to_count:
                            result_to_count[result] = 0
                        result_to_count[result] += 1
            log.info(f"{v}: {result_to_count}")

            norm_name = k
            if result_to_count:
                norm_name = max(result_to_count, key=result_to_count.get)

            idx[norm_name] = v

        json_file = JSONFile(os.path.join("data", "name_idx.json"))
        json_file.write(idx)
        print(f"Wrote {json_file.path}")


if __name__ == "__main__":
    NameSimilarity().run()
