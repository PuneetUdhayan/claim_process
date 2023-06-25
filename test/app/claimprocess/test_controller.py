import os

import pytest
import requests

from app.claimprocess import controller
from app.claimprocess import exceptions


def test_generate_claim_id():
    claim_id = controller.generate_claim_id()
    claim_id_2 = controller.generate_claim_id()
    assert isinstance(claim_id, str)
    assert claim_id is not None
    assert claim_id != claim_id_2


def test_compute_net_fees_happy_flow():
    provider_fees = 100.0
    member_coinsurance = 20.0
    member_copay = 10.0
    allowed_fees = 50.0

    expected_net_fees = 80.00
    actual_net_fees = controller.compute_net_fees(
        provider_fees, member_coinsurance, member_copay, allowed_fees
    )

    assert expected_net_fees == actual_net_fees


def test_compute_net_fees_large_allowed():
    provider_fees = 100.0
    member_coinsurance = 20.0
    member_copay = 10.0
    allowed_fees = 200.0

    expected_net_fees = 0
    actual_net_fees = controller.compute_net_fees(
        provider_fees, member_coinsurance, member_copay, allowed_fees
    )

    assert expected_net_fees == actual_net_fees


def test_call_payments(mocker):
    claim_details = mocker.Mock()
    response = mocker.Mock(status_code=200)
    mocker.patch("requests.post", return_value=response)

    mocker.patch.dict(
        os.environ,
        {
            "PAYMENT_GATEWAY_ENDPOINT": "http://example.com",
            "PAYMENT_GATEWAY_KEY": "your_access_token",
        },
    )

    controller.call_payments(claim_details)

    requests.post.assert_called_once_with(
        "http://example.com",
        params={"access_token": "your_access_token"},
        data=claim_details.json(),
    )
    assert response.status_code == 200


def test_call_payments_error(mocker):
    claim_details = mocker.Mock()
    response = mocker.Mock(status_code=400)
    mocker.patch("requests.post", return_value=response)

    mocker.patch.dict(
        os.environ,
        {
            "PAYMENT_GATEWAY_ENDPOINT": "http://example.com",
            "PAYMENT_GATEWAY_KEY": "your_access_token",
        },
    )

    with pytest.raises(exceptions.PaymentGatewayUnreachable):
        controller.call_payments(claim_details)
