from dataclasses import dataclass
from functools import cached_property

from utils import Log

from utils_future import Storable

log = Log("Parliament")


@dataclass
class Parliament(Storable):
    num: int
    election_year: str
    date_start: str
    date_end: str

    @cached_property
    def id(self):
        return f"{self.num:02d}-{self.election_year}"

    @staticmethod
    def get_election_year(num):
        return {
            9: 1989,
            10: 1994,
            11: 2000,
            12: 2001,
            13: 2004,
            14: 2010,
            15: 2015,
            16: 2020,
            17: 2024,
        }[num]

    @staticmethod
    def get_date_start_and_end(num):
        return {
            9: ("1989-02-15", "1994-06-24"),
            10: ("1994-08-25", "2000-08-18"),
            11: ("2000-10-18", "2001-10-10"),
            12: ("2001-12-19", "2004-02-07"),
            13: ("2004-04-22", "2010-02-09"),
            14: ("2010-04-22", "2015-06-26"),
            15: ("2015-09-01", "2020-03-03"),
            16: ("2020-08-20", "2024-09-24"),
            17: ("2024-11-24", "2029-11-24"),
        }[num]

    @classmethod
    def from_num(Class, num):
        date_start, date_end = Class.get_date_start_and_end(num)
        parliament = Class(
            num, Parliament.get_election_year(num), date_start, date_end
        )
        parliament.store()
        return parliament
