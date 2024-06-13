import subprocess
import time

import httpx
import pytest
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from dateutil.parser import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.orm import mapper_registry, mappers

API_BASE_URL = "http://127.0.0.1:8000"

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


def is_service_ready(attempts=5, delay=5):
    while attempts:
        try:
            httpx.get(API_BASE_URL + "/health").raise_for_status()
            return
        except Exception:
            attempts -= 1
            time.sleep(delay)
    subprocess.run(["make", "down-test-stack"], check=True)
    raise pytest.fail("Service did not become available in time.")


@pytest.fixture(scope="session", autouse=True)
def bring_up_crms_stack(request: SubRequest):
    has_e2e_test = False
    for test_fn in request.session.items:
        for marker in test_fn.own_markers:
            if marker.name == "e2e":
                has_e2e_test = True

    if not has_e2e_test:
        return

    subprocess.run(["make", "up-test-stack"], check=True)
    is_service_ready()
    # TODO: Populate some test data
    yield
    subprocess.run(["make", "down-test-stack"], check=True)


@pytest.fixture
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


@pytest.fixture
def api_test_data():
    return {
        "license": {
            "licenses": [
                {
                    "studio": "DISNEY",
                    "start_date": "2021-01-01T12:34:56.123445Z",
                    "end_date": "2022-01-01T12:35:55.123445Z",
                }
            ]
        }
    }
