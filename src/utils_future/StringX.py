from functools import cached_property

from utils import Log, TimeFormat

log = Log("StringX")


class StringX:
    TIME_FORMAT_DEFAULT = "%Y-%m-%d"
    TIME_FORMAT_LIST = [TIME_FORMAT_DEFAULT, "%d %B %Y", "%B %d, %Y", "%B %Y"]

    def __init__(self, x):
        self.x = (
            str(x).replace(",", "").replace("?", "").replace("\n", "").strip()
        )

    @cached_property
    def int(self) -> int:

        try:
            return int(self.x)
        except ValueError:
            return None

    @cached_property
    def snake_case(self) -> str:
        s1 = self.x
        s2 = ""
        for i, c in enumerate(s1):
            if c.isupper():
                s2 += " "
            s2 += c
        return s2.strip().lower().replace(" ", "_")

    @cached_property
    def date(self) -> str:
        if not self.x:
            return None
        for fmt in StringX.TIME_FORMAT_LIST:
            try:
                return TimeFormat(fmt).parse(self.x)
            except ValueError:
                pass

        log.error("Could not parse: " + self.x)
        return None

    @cached_property
    def date_str(self):
        date = self.date
        if not date:
            return None
        return TimeFormat(StringX.TIME_FORMAT_DEFAULT).format(date)
