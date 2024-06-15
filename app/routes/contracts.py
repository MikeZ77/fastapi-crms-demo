from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from pydantic import UUID4, AliasChoices, BaseModel, Field, constr

from app.services.contracts import add_contract, add_offers, get_contract
from app.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


class Contract(BaseModel):
    licenses: list[License] = []


# We can use pydantic for "data" validation and have the domain model validate
# business rules. #e.g. use AwareDatetime to validate datetimes have a timezone
class License(BaseModel):
    studio: str = constr(max_length=255)
    start_date: datetime
    end_date: datetime = Field(alias=AliasChoices("_end_date", "end_date"))


class Offer(BaseModel):
    name: str = constr(max_length=20)
    price: float
    start_date: datetime
    end_date: datetime


class OfferPayload(BaseModel):
    contract_id: UUID4
    studio: str
    offers: list[Offer]


# I use the convention of "insert" for the endpoint because of CRUD, but in
# SqlAlchemy land it uses "add"
@router.post("/", status_code=201)
def insert_contract(contract: Contract):
    """
    Inserts a contract and associated Licenses. This will show up in our
    http://localhost:8000/docs.
    """
    # It is fine to call multiple services and add try except handling to our entry point
    return add_contract(contract, SqlAlchemyUnitOfWork())


# Using Contract as a response model is useful for filtering what is sent to the client
@router.get("/{contract_id}", status_code=200)
def read_contract(contract_id: UUID4) -> Contract:
    return get_contract(contract_id, SqlAlchemyUnitOfWork())


@router.post("/license/offer", status_code=201)
def insert_offers(offer_payload: OfferPayload):
    add_offers(
        offer_payload.contract_id,
        offer_payload.studio,
        offer_payload.offers,
        SqlAlchemyUnitOfWork(),
    )
