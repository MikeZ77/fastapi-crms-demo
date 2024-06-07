from __future__ import annotations

from app.services.unit_of_work import AbstractUnitOfWork


# For the purposes of this example code, contract is just an empty shell.
# You would expect it to have many more data attributes.
def add_contract(uow: AbstractUnitOfWork):
    with uow:
        id = uow.contracts.add_contract()
        uow.commit()
    return id
