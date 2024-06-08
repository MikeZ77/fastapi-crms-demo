from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel, constr

from app.services.contracts import add_contract
from app.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


class Contract(BaseModel):
    licenses: list[License] = []


class License(BaseModel):
    studio: str = constr(max_length=255)
    start_date: datetime
    end_date: datetime


# I use the convention of "insert" for the endpoint because of CRUD, but in
# SqlAlchemy land it uses "add"
@router.post("/", status_code=201)
def insert_contract(contract: Contract):
    id = add_contract(contract, SqlAlchemyUnitOfWork())
    return id
