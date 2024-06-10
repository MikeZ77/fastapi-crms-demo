from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from pydantic import UUID4, BaseModel, ConfigDict, Field, constr

from app.services.contracts import add_contract, get_contract
from app.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


class Contract(BaseModel):
    licenses: list[License] = []


# We can use pydantic for "data" validation and have the domain model validate
# business rules. #e.g. use AwareDatetime to validate datetimes have a timezone
class License(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    studio: str = constr(max_length=255)
    start_date: datetime
    end_date_: datetime = Field(alias="end_date")


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
