from pydantic import UUID4

from app.domain.content import Content
from app.domain.contracts import Offer
from app.services.unit_of_work import AbstractUnitOfWork


class DomainError(Exception): ...


def assign_offer_to_content(
    contract_id: UUID4,
    license_id: UUID4,
    offer: dict,
    content: Content,
    uow: AbstractUnitOfWork,
):
    contract = uow.contracts.get_contract(contract_id)
    offer = Offer(**offer)
    for license in contract.licenses:
        if license.license_id == license_id and offer in license._offers:
            content.offer_name = offer.name
            return

    raise DomainError("Offer not found in contract")
