from functools import cached_property

from bs4 import BeautifulSoup
from utils import WWW, Log

from politicians_lk.core import Politician

log = Log("WikiParliamentDataTable")


class WikiParliamentDataTable:
    def __init__(self, num):
        self.num = num

    @cached_property
    def url(self):
        return (
            "https://en.wikipedia.org/wiki"
            + f"/{self.num}th_Parliament_of_Sri_Lanka"
        )

    @cached_property
    def html(self):
        html = WWW(self.url).read()
        n = len(html)
        log.info(f"Downloaded {n / 1000:.1f}KB from {self.url}")
        return html

    @cached_property
    def soup(self):
        return BeautifulSoup(self.html, "html.parser")

    @staticmethod
    def parse_row(tr):
        text_list = [td.text for td in tr.find_all("td")]
        if len(text_list) != 14:
            return None
        [
            full_name,
            ed_code,
            pref_votes,
            date_member_from,
            date_member_to,
            __,
            elected_party_id,
            __,
            elected_alliance_id,
            __,
            current_party_id,
            __,
            current_alliance_id,
            notes,
        ] = text_list
        return dict(
            full_name=full_name,
            ed_code=ed_code,
            pref_votes=pref_votes,
            date_member_from=date_member_from,
            date_member_to=date_member_to,
            elected_party_id=elected_party_id,
            elected_alliance_id=elected_alliance_id,
            current_party_id=current_party_id,
            current_alliance_id=current_alliance_id,
            notes=notes,
        )

    @cached_property
    def raw_data_list(self) -> list[dict]:
        soup = self.soup
        tables = soup.find_all("table", {"class": "plainrowheaders"})
        tbody = tables[0].find("tbody")
        tr_list = tbody.find_all("tr")
        d_list = []
        for tr in tr_list:
            d = self.parse_row(tr)
            if d:
                d_list.append(d)
        n = len(d_list)
        log.debug(f"Found {n} rows in the table")
        return d_list

    @cached_property
    def politician_list(self) -> list[Politician]:
        return [
            Politician.from_full_name_fuzzy(d["full_name"])
            for d in self.raw_data_list
        ]


if __name__ == "__main__":
    w = WikiParliamentDataTable(16)
    print(w.politician_list)
