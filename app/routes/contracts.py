from __future__ import annotations

from fastapi import APIRouter
from pydantic import AwareDatetime, BaseModel, constr

from app.services.contracts import add_contract
from app.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


class Contract(BaseModel):
    licenses: list[License] = []


# We can use pydantic for "data" validation and have the domain model validate
# business rules
class License(BaseModel):
    studio: str = constr(max_length=255)
    start_date: AwareDatetime
    end_date: AwareDatetime


# I use the convention of "insert" for the endpoint because of CRUD, but in
# SqlAlchemy land it uses "add"
@router.post("/", status_code=201)
def insert_contract(contract: Contract):
    return add_contract(contract, SqlAlchemyUnitOfWork())
