from __future__ import annotations

from fastapi import APIRouter
from pydantic import UUID4

from app.routes.types import ContractRequest, ContractResponse, OfferRequest
from app.services.contracts import add_contract, add_offers, get_contract
from app.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


# I use the convention of "insert" for the endpoint because of CRUD, but in
# SqlAlchemy land it uses "add"
@router.post("/", status_code=201)
def insert_contract(contract: ContractRequest):
    """
    Inserts a contract and associated Licenses. This will show up in our
    http://localhost:8000/docs.
    """
    # It is fine to call multiple services and add try except handling to our entry point
    return add_contract(contract, SqlAlchemyUnitOfWork())


# Using Contract as a response model is useful for filtering what is sent to the client
@router.get("/{contract_id}", status_code=200)
def read_contract(contract_id: UUID4) -> ContractResponse:
    return get_contract(contract_id, SqlAlchemyUnitOfWork())


@router.post("/license/offer", status_code=201)
def insert_offers(offer_payload: OfferRequest):
    add_offers(offer_payload, SqlAlchemyUnitOfWork())
