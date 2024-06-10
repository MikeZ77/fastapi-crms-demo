from __future__ import annotations

from app.domain.contracts import Contract, License
from app.services.unit_of_work import AbstractUnitOfWork


# For the purposes of this example code, contract is just an empty shell.
# You would expect it to have many more data attributes.
def add_contract(contract: Contract, uow: AbstractUnitOfWork):
    with uow:
        licenses = [License(**(license.__dict__)) for license in contract.licenses]
        contract = Contract(licenses)
        id = uow.contracts.add_contract(contract)
        uow.commit()
    return id


def get_contract(contract_id: str, uow: AbstractUnitOfWork):
    with uow:
        # The SQLAlchemy model cannot be used outside the session
        # TODO: Find or use a method to serialize the SQLAlchemy model to a dict
        contract = uow.contracts.get_contract(contract_id)
        licenses = [license.__dict__ for license in contract.licenses]
        return {**contract.__dict__, "licenses": licenses}
