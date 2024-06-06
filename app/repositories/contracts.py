import abc

from app.domain import contracts as model


class AbstractAggregateRepository(abc.ABC):
    @abc.abstractmethod
    def add_contract(self, contract: model.Contract):
        raise NotImplementedError

    @abc.abstractmethod
    def get_contract(self, contract_id: int):
        raise NotImplementedError


class AggregateRepository(AbstractAggregateRepository):
    def __init__(self, session):
        self.session = session

    def add_contract(self, contract: model.Contract):
        self.session.add(contract)

    def get_contract(self, contract_id: int):
        return self.session.query(model.Contract).filter_by(id=contract_id).one()
        # return self.session.execute(
        #     "SELECT * FROM contracts WHERE id=:val", {"id": contract_id}
        # )
