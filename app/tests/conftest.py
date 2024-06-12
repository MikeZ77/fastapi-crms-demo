import subprocess
from typing import Callable

import pytest
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from dateutil.parser import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.orm import mapper_registry, mappers

# NOTE: With more utilities, fixtures, or hooks, you would likely want to move these
# into their own files and import them into a main conftest.py.


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    for mapper in mappers:
        mapper()
    yield sessionmaker(bind=in_memory_db)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()


def pytest_collection_modifyitems(items: list[Function]):
    for test_fn in items:
        if "test_service_" in test_fn.name:
            test_fn.add_marker(pytest.mark.integration)

        if "test_api_" in test_fn.name:
            test_fn.add_marker(pytest.mark.e2e)

        if "test_domain_" in test_fn.name:
            test_fn.add_marker(pytest.mark.unit)


@pytest.fixture(scope="session", autouse=True)
def bring_up_api_stack(request: SubRequest):
    has_e2e_test = False
    for test_fn in request.session.items:
        for marker in test_fn.own_markers:
            if marker.name == "e2e":
                has_e2e_test = True

    if not has_e2e_test:
        return

    print()
    ...


@pytest.fixture(scope="function")
def test_data():
    return {
        "license": {
            "studio": "DISNEY",
            "start_date": parse("2019-01-01T12:34:56.123445Z"),
            "end_date": parse("2025-01-01T12:34:55.123445Z"),
        },
        "old_offer": {
            "name": "DSC",
            "price": 9.99,
            "start_date": parse("2021-01-01T12:34:56.123445Z"),
            "end_date": parse("2022-01-01T12:34:55.123445Z"),
        },
        "current_offer": {
            "name": "PREM",
            "price": 4.99,
            "start_date": parse("2022-01-01T12:34:56.123445Z"),
            "end_date": parse("2022-10-01T12:34:56.123445Z"),
        },
        "future_offer": {
            "name": "STD_DSC",
            "price": 1.99,
            "start_date": parse("2023-01-01T12:34:56.123445Z"),
            "end_date": parse("2023-09-09T12:34:56.123445Z"),
        },
    }
