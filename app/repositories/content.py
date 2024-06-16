import abc

from sqlalchemy.orm.session import Session

from app.domain import content as model


class AbstractContentRepository(abc.ABC):
    @abc.abstractmethod
    def add_content(self, content: model.Content):
        raise NotImplementedError

    @abc.abstractmethod
    def get_content(self, content_id: int):
        raise NotImplementedError


class AggregateRepository(AbstractContentRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_content(self, contract: model.Content) -> int:
        self.session.add(contract)
        self.session.flush()
        return contract.content_id

    def get_content(self, content_id: str):
        return self.session.query(model.Content).filter_by(content_id=content_id).one()
