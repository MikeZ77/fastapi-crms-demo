from __future__ import annotations

from dataclasses import dataclass
from datetime import date


class Contracts:
    def __init__(self, licenses: list[Licenses], version: int):
        self.licenses = licenses
        self.version = version


class Licenses:
    def __init__(self, contract_id: int, studio: str, start_date: str, end_date: str):
        self.contract_id = contract_id
        self.studio = studio
        self.start_date = start_date
        self.end_date = end_date
        self._offers: set[Offers] = set()


# Dataclasses are good options for value objects. This is because they are compared
# based on the equality of their data and are immutable. If we want to change an offer,
# we have to delete it then create it again.
# Also, having frozen=True and eq=True (default) implements __hash__ so we can us it in
# sets or as dict keys.
@dataclass(frozen=True)
class Offers:
    name: str
    price: int
    start_date: date
    end_date: date
