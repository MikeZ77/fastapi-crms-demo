import abc

from sqlalchemy.orm.session import Session

from app.domain import contracts as model


class AbstractAggregateRepository(abc.ABC):
    @abc.abstractmethod
    def add_contract(self, contract: model.Contract):
        raise NotImplementedError

    @abc.abstractmethod
    def get_contract(self, contract_id: int):
        raise NotImplementedError


class AggregateRepository(AbstractAggregateRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_contract(self, contract: model.Contract) -> int:
        self.session.add(contract)
        self.session.flush()  # This syncs the in-memory state with the database
        return contract.contract_id  # but does not commit. So we can return the id.

    def get_contract(self, contract_id: int):
        return self.session.query(model.Contract).filter_by(id=contract_id).one()

        # If we wanted to use raw SQL ...
        # return self.session.execute(
        #     "SELECT * FROM contracts WHERE id=:val", {"id": contract_id}
        # )
