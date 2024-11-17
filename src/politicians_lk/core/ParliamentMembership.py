from dataclasses import dataclass
from functools import cached_property

from utils import Log, TimeFormat, TimeUnit

from politicians_lk.core.Politician import Politician
from utils_future import Storable, StringX

log = Log("ParliamentMembership")


@dataclass
class ParliamentMembership(Storable):
    politician_id: str
    parliament_num: int
    ed_id: str
    pref_votes: int
    date_member_from: str
    date_member_to: str
    elected_party_id: str
    current_party_id: str

    @cached_property
    def id(self):
        return f"{self.politician_id}.{self.parliament_num:02d}"

    @classmethod
    def from_d(Class, parliament, d):
        politician = Politician.from_full_name_fuzzy(d["full_name"])
        parliament_membership = Class(
            politician_id=politician.id,
            parliament_num=parliament.num,
            ed_id=d["ed_code"],  # TODO: Change!
            pref_votes=d["pref_votes"],
            date_member_from=StringX(d["date_member_from"]).date_str,
            date_member_to=StringX(d["date_member_to"]).date_str,
            elected_party_id=d["elected_party_id"],
            current_party_id=d["current_party_id"],
        )
        parliament_membership.store()
        return parliament_membership

    @cached_property
    def duration_days(self):
        try:
            duration = (
                TimeFormat.DATE.parse(self.date_member_to).ut
                - TimeFormat.DATE.parse(self.date_member_from).ut
            )
            duration_days = duration / TimeUnit.SECONDS_IN.DAY
            return int(duration_days)
        except Exception:
            return None

    @cached_property
    def custom_d(self):

        return dict(
            duration_days=self.duration_days,
        )
