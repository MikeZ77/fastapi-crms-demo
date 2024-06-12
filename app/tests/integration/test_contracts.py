import uuid

from pydantic import UUID4

from app.domain.contracts import Contract
from app.repositories.contracts import AbstractAggregateRepository
from app.routes.contracts import Contract as ContractModel
from app.routes.contracts import License as LicenseModel
from app.services.contracts import add_contract, get_contract
from app.services.unit_of_work import AbstractUnitOfWork


class FakeRepository(AbstractAggregateRepository):
    def __init__(self, contracts: list[Contract]):
        self._contracts = set(contracts)

    def add_contract(self, contract: Contract):
        self._contracts.add(contract)
        return contract.contract_id

    def get_contract(self, id: UUID4):
        return next(
            (contract for contract in self._contracts if contract.contract_id == id),
            None,
        )


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.contracts = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self): ...


def test_service_can_insert_contract(test_data):
    uow = FakeUnitOfWork()
    contract = ContractModel(licenses=[LicenseModel(**test_data["license"])])
    id = add_contract(contract, uow)
    assert isinstance(id, uuid.UUID)


def test_service_can_retrieve_contract(test_data):
    uow = FakeUnitOfWork()
    contract = ContractModel(licenses=[LicenseModel(**test_data["license"])])
    id = add_contract(contract, uow)
    get_contract(id, uow)
