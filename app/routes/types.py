from __future__ import annotations

from datetime import datetime

from pydantic import UUID4, AliasChoices, BaseModel, Field, constr


class ContractRequest(BaseModel):
    licenses: list[_License] = []


ContractResponse = ContractRequest


# We can use pydantic for "data" validation and have the domain model validate
# business rules. #e.g. use AwareDatetime to validate datetimes have a timezone
class _License(BaseModel):
    studio: str = constr(max_length=255)
    start_date: datetime
    end_date: datetime = Field(alias=AliasChoices("_end_date", "end_date"))


class _Offer(BaseModel):
    name: str = constr(max_length=20)
    price: float
    start_date: datetime
    end_date: datetime


class OfferRequest(BaseModel):
    contract_id: UUID4
    studio: str
    offers: list[_Offer]


class ContentRequest(BaseModel):
    contract_id: UUID4
    license_id: UUID4
    offer: _Offer
