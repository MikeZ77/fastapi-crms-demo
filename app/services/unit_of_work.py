from __future__ import annotations

import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.repositories.contracts import AggregateRepository as ContractRepository
from app.utils import config

SessionFactory = sessionmaker(bind=create_engine(config.get_postgres_uri()))


class AbstractUnitOfWork(abc.ABC):
    contracts: ContractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *_):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=SessionFactory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.contracts = ContractRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
