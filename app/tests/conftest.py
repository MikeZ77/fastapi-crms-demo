import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.orm import mappers, registries


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    for registry in registries:
        registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    for start_mapper in mappers:
        start_mapper()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()
