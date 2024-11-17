from functools import cached_property

from bs4 import BeautifulSoup
from utils import WWW, Log

from politicians_lk.core import Parliament, ParliamentMembership, Politician
from utils_future import StringX

log = Log("WikiParliamentDataTable")


class WikiParliamentDataTable:
    def __init__(self, parliament):
        self.parliament = parliament

    @cached_property
    def url(self):
        return (
            "https://en.wikipedia.org/wiki"
            + f"/{self.parliament.num}th_Parliament_of_Sri_Lanka"
        )

    @cached_property
    def html(self):
        html = WWW(self.url).read()
        n = len(html)
        log.debug(f"Downloaded {n / 1000:.1f}KB from {self.url}")
        return html

    @cached_property
    def soup(self):
        return BeautifulSoup(self.html, "html.parser")

    @staticmethod
    def parse_row_14(text_list):

        return dict(
            full_name=text_list[0],
            ed_code=text_list[1],
            pref_votes=StringX(text_list[2]).int,
            date_member_from=text_list[3],
            date_member_to=text_list[4],
            elected_party_id=text_list[6],
            elected_alliance_id=text_list[8],
            current_party_id=text_list[10],
            current_alliance_id=text_list[12],
            notes=text_list[13],
        )

    @staticmethod
    def parse_row_10(text_list):

        return dict(
            full_name=text_list[0],
            ed_code=text_list[1],
            pref_votes=StringX(text_list[2]).int,
            date_member_from=text_list[3],
            date_member_to=text_list[4],
            elected_party_id=text_list[6],
            current_party_id=text_list[8],
            notes=text_list[9],
        )

    @staticmethod
    def parse_row(text_list):
        if len(text_list) == 14:
            return WikiParliamentDataTable.parse_row_14(text_list)
        if len(text_list) == 10:
            return WikiParliamentDataTable.parse_row_10(text_list)

        return None

    @cached_property
    def table(self):
        soup = self.soup
        return soup.find_all("table", {"class": "wikitable"})[-1]

    @cached_property
    def raw_data_list(self) -> list[dict]:
        tr_list = self.table.find_all("tr")
        d_list = []
        for tr in tr_list:
            td_list = tr.find_all("td")
            text_list = [td.text for td in td_list]
            d = self.parse_row(text_list)
            if d and d["full_name"] != "?":
                d_list.append(d)
        n = len(d_list)
        log.debug(f"Found {n} rows in the table")
        return d_list

    @cached_property
    def politician_list(self) -> list[Politician]:
        politician_list = [
            Politician.from_full_name_fuzzy(d["full_name"])
            for d in self.raw_data_list
        ]
        log.info(f"Found {len(politician_list)} politicians")
        return politician_list

    @cached_property
    def parliament_membership_list(self) -> list[ParliamentMembership]:
        parliament_membership_list = [
            ParliamentMembership.from_d(self.parliament, d)
            for d in self.raw_data_list
        ]
        log.info(f"Found {len(parliament_membership_list)} memberships")
        return parliament_membership_list


if __name__ == "__main__":
    for num in [17]:
        w = WikiParliamentDataTable(Parliament.from_num(num))
        w.politician_list
        w.parliament_membership_list
