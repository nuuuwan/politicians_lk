from dataclasses import dataclass

from utils import Log

from utils_future import Name, Storable

log = Log("Person")


@dataclass
class Person(Storable):
    id: str
    full_name: str
    wiki_page: str
    dob: str
    dod: str
    gender: str

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def from_full_name_fuzzy(Class, full_name: str) -> "Person":
        full_name = full_name.replace(".", "").replace("\n", "").strip()

        if "," in full_name:
            full_name = (
                full_name.split(",")[1] + " " + full_name.split(",")[0]
            )
        full_name = full_name.strip()

        full_name = Name.get_norm_name(full_name)
        id = full_name.replace(" ", "-")

        person = Class(
            id=id,
            full_name=full_name,
            wiki_page=None,
            gender=None,
            dob=None,
            dod=None,
        )
        person.store()
        return person
