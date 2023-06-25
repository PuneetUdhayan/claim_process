import os
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_claim_process_without_quadrant(set_up_env):
    payload = {
        "service date": "3/28/18 0:00",
        "submitted procedure": "D0180",
        "quadrant": None,
        "Plan/Group #": "GRP-1000",
        "Subscriber#": 3730189502,
        "Provider NPI": 1497775530,
        "provider fees": "$100.00 ",
        "Allowed fees": "$100.00 ",
        "member coinsurance": "$0.00 ",
        "member copay": "$0.00 ",
    }
    response = client.post(
        "/claim",
        params={"access_token": os.environ["API_KEY"]},
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    claim = response.json()
    assert claim["status"] == True
    assert claim["data"]["service_date"] == "2018-03-28T00:00:00"
    assert claim["data"]["submitted_procedure"] == "D0180"
    assert claim["data"]["quadrant"] == None
    assert claim["data"]["plan_group_number"] == "GRP-1000"
    assert claim["data"]["subscriber_number"] == 3730189502
    assert claim["data"]["provider_npi"] == 1497775530
    assert claim["data"]["currency"] == "$"
    assert claim["data"]["provider_fees"] == 100
    assert claim["data"]["allowed_fees"] == 100
    assert claim["data"]["member_coinsurance"] == 0
    assert claim["data"]["member_copay"] == 0
    assert isinstance(claim["data"]["claim_id"], str)
    assert claim["data"]["net_fees"] == 0


def test_claim_process_with_quadrant(set_up_env):
    payload = {
        "service date": "3/28/18 0:00",
        "submitted procedure": "D0180",
        "quadrant": "DM",
        "Plan/Group #": "GRP-1000",
        "Subscriber#": 3730189502,
        "Provider NPI": 1497775531,
        "provider fees": "$100.00 ",
        "Allowed fees": "$10.00 ",
        "member coinsurance": "$0.00 ",
        "member copay": "$0.00 ",
    }
    response = client.post(
        "/claim",
        params={"access_token": os.environ["API_KEY"]},
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    claim = response.json()
    assert claim["status"] == True
    assert claim["data"]["service_date"] == "2018-03-28T00:00:00"
    assert claim["data"]["submitted_procedure"] == "D0180"
    assert claim["data"]["quadrant"] == "DM"
    assert claim["data"]["plan_group_number"] == "GRP-1000"
    assert claim["data"]["subscriber_number"] == 3730189502
    assert claim["data"]["provider_npi"] == 1497775531
    assert claim["data"]["currency"] == "$"
    assert claim["data"]["provider_fees"] == 100
    assert claim["data"]["allowed_fees"] == 10
    assert claim["data"]["member_coinsurance"] == 0
    assert claim["data"]["member_copay"] == 0
    assert isinstance(claim["data"]["claim_id"], str)
    assert claim["data"]["net_fees"] == 90


def test_claim_process_provider_npi_validation(set_up_env):
    payload = {
        "service date": "3/28/18 0:00",
        "submitted procedure": "D0180",
        "quadrant": None,
        "Plan/Group #": "GRP-1000",
        "Subscriber#": 3730189502,
        "Provider NPI": 149777553,
        "provider fees": "$100.00 ",
        "Allowed fees": "$100.00 ",
        "member coinsurance": "$0.00 ",
        "member copay": "$0.00 ",
    }
    response = client.post(
        "/claim",
        params={"access_token": os.environ["API_KEY"]},
        data=json.dumps(payload),
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "provider_npi"],
                "msg": "Provider NPI must be exactly 10 digits long",
                "type": "value_error",
            }
        ]
    }


def test_claim_process_submitted_procedure_validation(set_up_env):
    payload = {
        "service date": "3/28/18 0:00",
        "submitted procedure": "H0180",
        "quadrant": None,
        "Plan/Group #": "GRP-1000",
        "Subscriber#": 3730189502,
        "Provider NPI": 1497775530,
        "provider fees": "$100.00 ",
        "Allowed fees": "$100.00 ",
        "member coinsurance": "$0.00 ",
        "member copay": "$0.00 ",
    }
    response = client.post(
        "/claim",
        params={"access_token": os.environ["API_KEY"]},
        data=json.dumps(payload),
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "submitted_procedure"],
                "msg": 'string does not match regex "^D.*$"',
                "type": "value_error.str.regex",
                "ctx": {"pattern": "^D.*$"},
            }
        ]
    }
