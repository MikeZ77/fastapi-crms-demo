from __future__ import annotations

from pydantic import UUID4

from app.domain.contracts import Contract, License, Offer
from app.services.unit_of_work import AbstractUnitOfWork


# For the purposes of this example code, contract is just an empty shell.
# You would expect it to have many more data attributes.
def add_contract(contract: Contract, uow: AbstractUnitOfWork):
    with uow:
        licenses = [License.from_pydantic(license) for license in contract.licenses]
        contract = Contract(licenses)
        id = uow.contracts.add_contract(contract)
        uow.commit()
    return id


def get_contract(contract_id: UUID4, uow: AbstractUnitOfWork):
    with uow:
        # NOTE: This is important to understand. get_contract does a left join on licenses
        # since in this example we need to return licenses with the contract.
        # If we didn't do this left join, we could still get licenses by accessing
        # contract.licenses which calls the db to get licenses. This is the default aka
        # lazy loading because contract.licesnses doesnt exist until we call it.
        # This is why we can't use contract outside the uow/session. When we map our
        # data to our domain models, it becomes an SQLAlchemy object
        contract = uow.contracts.get_contract(contract_id)
        return contract.sqlalchemy_to_dict()


def add_offers(
    contract_id: UUID4, studio: str, offers: list[Offer], uow: AbstractUnitOfWork
):
    with uow:
        contract = uow.contracts.get_contract(contract_id)
        for offer in offers:
            contract.generate_offer(studio, Offer.from_pydantic(offer))
