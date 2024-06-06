from datetime import datetime

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


@pytest.fixture(scope="function")
def test_data():
    return {
        "license": {
            "contract_id": 1,
            "studio": "DISNEY",
            "start_date": datetime.fromisoformat("2019-01-01T12:34:56.123445"),
            "end_date": datetime.fromisoformat("2025-01-01T12:34:55.123445"),
        },
        "old_offer": {
            "name": "DSC",
            "price": 9.99,
            "start_date": datetime.fromisoformat("2021-01-01T12:34:56.123445"),
            "end_date": datetime.fromisoformat("2022-01-01T12:34:55.123445"),
        },
        "current_offer": {
            "name": "PREM",
            "price": 4.99,
            "start_date": datetime.fromisoformat("2022-01-01T12:34:56.123445"),
            "end_date": datetime.fromisoformat("2022-10-01T12:34:56.123445"),
        },
        "future_offer": {
            "name": "STD_DSC",
            "price": 1.99,
            "start_date": datetime.fromisoformat("2023-01-01T12:34:56.123445"),
            "end_date": datetime.fromisoformat("2023-09-09T12:34:56.123445"),
        },
    }
