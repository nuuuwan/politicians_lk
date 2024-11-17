from dataclasses import dataclass
from functools import cached_property

from utils import Log, TimeFormat, TimeUnit

from politicians_lk.core.Parliament import Parliament
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

    @staticmethod
    def get_ed_id(ed_code):
        ed_code = ed_code[:3]
        return {
            "COL": "EC-01",
            "GAM": "EC-02",
            "KAL": "EC-03",
            "KAN": "EC-04",
            "MTL": "EC-05",
            "NUW": "EC-06",
            "GAL": "EC-07",
            "MTR": "EC-08",
            "HAM": "EC-09",
            "JAF": "EC-10",
            "VAN": "EC-11",
            "BAT": "EC-12",
            "AMP": "EC-13",
            "TRI": "EC-14",
            "KUR": "EC-15",
            "PUT": "EC-16",
            "ANU": "EC-17",
            "POL": "EC-18",
            "BAD": "EC-19",
            "MON": "EC-20",
            "RAT": "EC-21",
            "KEG": "EC-22",
            "NAT": "LK",
        }[ed_code]

    @cached_property
    def parliament(self):
        return Parliament.from_num(self.parliament_num)

    @classmethod
    def get_date_member_from(_, politician, parliament, d):
        if parliament.num == 9:
            if politician.id == "Joseph-Pararajasingham":
                return "1990-05-11"

        if parliament.num == 10:
            if politician.id in ["P-P-Devaraj", "Ramaiah-Yogarajan"]:
                return "1994-10-28"
            if politician.id in ["Nihal-Galappaththi"]:
                return "1994-08-31"

        return parliament.date_start

    @classmethod
    def get_date_member_to(_, politician, parliament, d):
        if parliament.num == 10:

            if politician.id in ["J-P-V-Vipulaguna"]:
                return "1994-08-31"

        return parliament.date_end

    @classmethod
    def from_d(Class, parliament, d):
        politician = Politician.from_full_name_fuzzy(d["full_name"])
        parliament_membership = Class(
            politician_id=politician.id,
            parliament_num=parliament.num,
            ed_id=ParliamentMembership.get_ed_id(d["ed_code"]),
            pref_votes=d["pref_votes"],
            date_member_from=StringX(d["date_member_from"]).date_str
            or ParliamentMembership.get_date_member_from(
                politician, parliament, d
            ),
            date_member_to=StringX(d["date_member_to"]).date_str
            or ParliamentMembership.get_date_member_to(
                politician, parliament, d
            ),
            elected_party_id=d["elected_party_id"],
            current_party_id=d["current_party_id"],
        )
        parliament_membership.validate()
        parliament_membership.store()
        return parliament_membership

    def validate(self):
        errors = []
        # pref_votes
        if (
            self.ed_id != "LK"
            and self.pref_votes is None
            and self.date_member_from == self.parliament.date_start
        ):
            errors.append("pref_votes is None")

        if not self.elected_party_id:
            errors.append("elected_party_id is empty")

        if errors:
            log.error(f"❌ {self.id}: {len(errors)} errors")
            for i_error, error in enumerate(errors, start=1):
                log.error(f"\t{i_error}) {error}")

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

    @classmethod
    def get_sorter(Class):

        return lambda d: (
            d["parliament_num"],
            d["ed_id"],
            -(d["pref_votes"] or 0),
            d["date_member_from"],
        )
