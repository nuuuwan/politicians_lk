from dataclasses import dataclass

from elections_lk import ElectionParliamentary, Party
from utils import Log

from politicians_lk.core import Politician

log = Log("ElectionPerformance")


@dataclass
class ElectionPerformance:
    politician: Politician
    election: ElectionParliamentary
    party: Party
    ed_id: str
    pref_votes: int
