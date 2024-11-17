from dataclasses import dataclass
from functools import cached_property

from utils import Log

from utils_future import Storable

log = Log("Parliament")


@dataclass
class Parliament(Storable):
    num: int
    election_year: str

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

    @classmethod
    def from_num(Class, num):
        parliament = Class(num, Parliament.get_election_year(num))
        parliament.store()
        return parliament
