from functools import cached_property


class StringX:
    def __init__(self, x):
        self.x = str(x)

    @cached_property
    def int(self) -> int:
        x = self.x.replace(",", "").replace("\n", "").strip()
        try:
            return int(x)
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
