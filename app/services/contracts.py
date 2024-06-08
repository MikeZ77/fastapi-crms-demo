from __future__ import annotations

from app.domain.contracts import Contract, License
from app.services.unit_of_work import AbstractUnitOfWork


# For the purposes of this example code, contract is just an empty shell.
# You would expect it to have many more data attributes.
def add_contract(contract: Contract, uow: AbstractUnitOfWork):
    with uow:
        licenses = [License(*license) for license in contract.licenses]
        contract = Contract(licenses)
        id = uow.contracts.add_contract(contract)
        uow.commit()
    return id
