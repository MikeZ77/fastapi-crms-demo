import httpx

from app.tests.conftest import API_BASE_URL


def test_api_create_contract(api_test_data):
    res = httpx.post(
        f"{API_BASE_URL}/api/contract",
        json=api_test_data["license"],
        follow_redirects=True,
    )
    assert res.status_code == 201
