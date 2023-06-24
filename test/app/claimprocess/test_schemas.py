from datetime import datetime

import pytest

from app.claimprocess.schemas import ClaimPayload, process_field


def test_process_filed():
    assert process_field("service date") == "service_date"
    assert process_field("submitted procedure  ") == "submitted_procedure"
    assert process_field("""quadrant
    """) == "quadrant"
    assert process_field("Plan/Group #") == "plan_group_number"
    assert process_field("Subscriber#") == "subscriber_number"
    assert process_field("Provider NPI") == "provider_npi"


def test_claim_payload_column_parse():
    claim_payload = ClaimPayload.parse_obj(
        {
            "service date": "3/28/18 0:00",
            "submitted procedure": "D0180",
            "Plan/Group #": "GRP-1000",
            "Subscriber#": 3730189502,
            "Provider NPI": 1497775530,
            "provider fees": "$100.00 ",
            "Allowed fees": "$100.00 ",
            "member coinsurance": "$0.00",
            "member copay": "$0.00",
        }
    )
    assert claim_payload.service_date == datetime(
        day=28, month=3, year=2018, hour=0, minute=0
    )
    assert claim_payload.submitted_procedure == "D0180"
    assert claim_payload.plan_group_number == "GRP-1000"
    assert claim_payload.subscriber_number == 3730189502
    assert claim_payload.provider_npi == 1497775530
    assert claim_payload.allowed_fees == 100.00
    assert claim_payload.member_coinsurance == 0.00
    assert claim_payload.member_copay == 0.00
    assert claim_payload.currency == "$"
    assert claim_payload.quadrant == None

    claim_payload = ClaimPayload.parse_obj(
        {
            "service date": "3/28/18 0:00",
            "submitted procedure": "D0180",
            "Plan/Group #": "GRP-1000",
            "Subscriber#": 3730189502,
            "Provider NPI": 1497775530,
            "provider fees": "$100.00 ",
            "Allowed fees": "$100.00 ",
            "member coinsurance": "$0.00",
            "member copay": "$0.00",
            "quadrant":"UR"
        }
    )
    assert claim_payload.service_date == datetime(
        day=28, month=3, year=2018, hour=0, minute=0
    )
    assert claim_payload.submitted_procedure == "D0180"
    assert claim_payload.plan_group_number == "GRP-1000"
    assert claim_payload.subscriber_number == 3730189502
    assert claim_payload.provider_npi == 1497775530
    assert claim_payload.allowed_fees == 100.00
    assert claim_payload.member_coinsurance == 0.00
    assert claim_payload.member_copay == 0.00
    assert claim_payload.currency == "$"
    assert claim_payload.quadrant == "UR"


def test_claim_payload_procedure_validation():
    with pytest.raises(ValueError) as exc_info:
        claim_payload = ClaimPayload.parse_obj(
            {
                "service date": "3/28/18 0:00",
                "submitted procedure": "0180",
                "Plan/Group #": "GRP-1000",
                "Subscriber#": 3730189502,
                "Provider NPI": 1497775530,
                "provider fees": "$100.00 ",
                "Allowed fees": "$100.00 ",
                "member coinsurance": "$0.00",
                "member copay": "$0.00",
            }
        )


def test_claim_payload_provider_npi_validation():
    with pytest.raises(ValueError) as exc_info:
        claim_payload = ClaimPayload.parse_obj(
            {
                "service date": "3/28/18 0:00",
                "submitted procedure": "D0180",
                "Plan/Group #": "GRP-1000",
                "Subscriber#": 3730189502,
                "Provider NPI": 14977755,
                "provider fees": "$100.00 ",
                "Allowed fees": "$100.00 ",
                "member coinsurance": "$0.00",
                "member copay": "$0.00",
            }
        )