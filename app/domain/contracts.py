from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


# Creating custom exceptions that refelct the domain or business jargon is useful.
class InvalidLicenseDate(Exception): ...


class InvalidOfferData(Exception): ...


class DomainModel:
    @classmethod
    def from_pydantic(cls, model: BaseModel):
        return cls(**model.model_dump())

    def sqlalchemy_to_dict(self) -> dict:
        # NOTE: This utility method is not complete, it just shows how you could go about
        # serializing a SQLAlchemy model to a dict.
        def to_dict(attr):
            my_dict = {}
            if not isinstance(attr, DomainModel) and not (
                isinstance(attr, Iterable)
                and any(isinstance(item, DomainModel) for item in attr)
            ):
                return attr
            else:
                for field, value in attr.__dict__.items():
                    if isinstance(value, list):
                        my_dict[field] = [to_dict(item) for item in value]
                    elif isinstance(value, set):
                        my_dict[field] = {to_dict(item) for item in value}
                    else:
                        my_dict[field] = to_dict(value)
            return my_dict

        return to_dict(self)


class Contract(DomainModel):
    def __init__(self, licenses: list[License], version: int = 0):
        # Note: Never use mutable default arguments in Python
        self.contract_id = uuid.uuid4()
        self.licenses = licenses
        self.version = version

    def generate_offer(self, studio: str, offer: Offer):
        """
        Generates an offer for the requested studio by finding an availble time slot.

        Raises:
            InvalidOfferData
        """
        license = next(
            (license for license in self.licenses if license.studio == studio), None
        )

        if not license:
            raise InvalidOfferData(f"Studio {studio} not found for this contract")

        license.insert_offer(offer)
        self.version += 1


# TODO: It would be cleaner to use Descriptors instead of property setters
# but it seems like maybe SQLAlchemy keeps its own mapping state and we would need to
# set end_date in there instead. Like this end_date is not included in any queries.
class EndDateDescriptor:
    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance: License, value: datetime):
        # We can assume that the pydantic model has already validated the date format
        if value <= instance.start_date:
            raise InvalidLicenseDate("End date must be after start date")
        instance.__dict__[self.name] = value


class License(DomainModel):
    # end_date = EndDateDescriptor("end_date")

    def __init__(self, studio: str, start_date: datetime, end_date: datetime):
        self.license_id = uuid.uuid4()
        self.studio = studio
        self.start_date = start_date
        self._end_date = end_date
        self._offers: set[Offer] = set()

    # Getters can be useful for performing small calculations on existing properties
    @property
    def period(self):
        self.end_date - self.start_date

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value: datetime):
        if value <= self.start_date:
            raise InvalidLicenseDate("End date must be after start date")
        self._end_date = value

    def insert_offer(self, new_offer: Offer):
        # Checking for overlapping offers
        conflict = next(
            (
                offer
                for offer in self._offers
                if offer.end_date > new_offer.start_date
                and offer.start_date < new_offer.end_date
            ),
            None,
        )

        if not conflict:
            self._offers.add(new_offer)
            return

        raise InvalidOfferData(
            f"No time slot available for {new_offer.start_date} to {new_offer.end_date}"
        )


# This is a value object rather than an entitiy so a dataclass is useful.
# With frozen=True and eq=True (default) then __hash__ is implemented for us.
# @dataclass(frozen=True)
@dataclass(unsafe_hash=True)
class Offer(DomainModel):
    name: str
    price: int
    start_date: datetime
    end_date: datetime
