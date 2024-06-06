from datetime import datetime

import pytest

from app.domain.contracts import InvalidOfferData, License, Offer


def test_can_insert_offer_with_available_slot(test_data):
    license = create_license(test_data)
    old_offer, new_offer, future_offer = create_offers(test_data)

    license._offers.add(old_offer)
    license._offers.add(future_offer)
    assert license.insert_offer(new_offer) is None


def test_cannot_insert_overlapping_old_offer(test_data):
    test_data["old_offer"]["end_date"] = datetime.fromisoformat(
        "2022-05-01T12:34:56.123445"
    )
    license = create_license(test_data)
    old_offer, new_offer, future_offer = create_offers(test_data)

    license._offers.add(old_offer)
    license._offers.add(future_offer)
    pytest.raises(InvalidOfferData, license.insert_offer, new_offer)


def create_license(test_data) -> License:
    return License(**test_data["license"])


def create_offers(test_data) -> tuple[Offer, Offer, Offer]:
    return (
        Offer(**test_data["old_offer"]),
        Offer(**test_data["current_offer"]),
        Offer(**test_data["future_offer"]),
    )
