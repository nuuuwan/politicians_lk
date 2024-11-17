from dataclasses import dataclass
from functools import cached_property

from utils import Log

from politicians_lk.core.Politician import Politician
from utils_future import Storable

log = Log("ParliamentMembership")


@dataclass
class ParliamentMembership(Storable):
    parliament_num: int
    politician_id: str
    ed_id: str
    pref_votes: int
    date_member_from: str
    date_member_to: str
    elected_party_id: str
    current_party_id: str

    @cached_property
    def id(self):
        return f"{self.parliament_num:02d}-{self.politician_id}"

    @classmethod
    def from_d(cls, parliament, d):
        politician = Politician.from_full_name_fuzzy(d["full_name"])
        parliament_membership = cls(
            parliament_num=parliament.num,
            politician_id=politician.id,
            ed_id=d["ed_code"],  # TODO: Change!
            pref_votes=d["pref_votes"],
            date_member_from=d["date_member_from"],
            date_member_to=d["date_member_to"],
            elected_party_id=d["elected_party_id"],
            current_party_id=d["current_party_id"],
        )
        parliament_membership.store()
        return parliament_membership
