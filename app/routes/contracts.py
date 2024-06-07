from fastapi import APIRouter
from pydantic import BaseModel

from app.services.contracts import add_contract
from app.services.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


# I use the convention of "insert" for the endpoint because of CRUD, but in
# SqlAlchemy land it uses "add"
@router.post("/", status_code=201)
def insert_contract():
    id = add_contract(SqlAlchemyUnitOfWork())
    return id
