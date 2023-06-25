import os
import uuid
import requests

from sqlalchemy.orm import Session

from app.schema import StandardResponse
from app.claimprocess import transaction
from app.claimprocess import exceptions
from app.claimprocess.schemas import ClaimPayload, ClaimDetails


def generate_claim_id() -> str:
    """Return a unique string using uuid4

    Returns:
        str: unique uuid string
    """
    return uuid.uuid4().hex


def compute_net_fees(
    provider_fees: float,
    member_coinsurance: float,
    member_copay: float,
    allowed_fees: float,
):
    """Computes net fees using the formula
    “net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”

    Args:
        provider_fees (float): “provider fees”
        member_coinsurance (float): “member coinsurance”
        member_copay (float): “member copay”
        allowed_fees (float): “Allowed fees”

    Returns:
        float: “net fee”
    """
    return max((provider_fees + member_coinsurance + member_copay - allowed_fees), 0)


def call_payments(claim_details: ClaimDetails):
    """This function calls the payment service with the claim_details

    Args:
        claim_details (ClaimDetails): Details of the claim including net fees and claim id
    """
    res = requests.post(
        os.environ["PAYMENT_GATEWAY_ENDPOINT"],
        params={"access_token": os.environ["PAYMENT_GATEWAY_KEY"]},
        data=claim_details.json(),
    )
    if res.status_code != 200:
        raise exceptions.PaymentGatewayUnreachable()


def claim_process(claim_payload: ClaimPayload, db: Session):
    """Controller function for processing claims

    Actions performed:
    1. Get claim id
    2. Get net fees
    3. Add entry for claim in DB
    4. Increment net fees for provider in DB
    5. Call payments service

    NOTE:
    I end up writing these big controllers that call other smaller functions
    can you please suggest an alternative to me. I would greatly appreciate that.

    Args:
        claim_payload (ClaimPayload): _description_
        db (Session): _description_

    Returns:
        _type_: _description_
    """
    claim_id = generate_claim_id()

    net_fees = compute_net_fees(
        provider_fees=claim_payload.provider_fees,
        member_coinsurance=claim_payload.member_coinsurance,
        member_copay=claim_payload.member_copay,
        allowed_fees=claim_payload.allowed_fees,
    )

    transaction.create_claim(
        claim_id=claim_id,
        service_date=claim_payload.service_date,
        submitted_procedure=claim_payload.submitted_procedure,
        plan_group_number=claim_payload.plan_group_number,
        subscriber_number=claim_payload.subscriber_number,
        provider_npi=claim_payload.provider_npi,
        currency=claim_payload.currency,
        provider_fees=claim_payload.provider_fees,
        allowed_fees=claim_payload.allowed_fees,
        member_coinsurance=claim_payload.member_coinsurance,
        member_copay=claim_payload.member_copay,
        net_fees=net_fees,
        db=db,
    )

    transaction.increment_net_fee_for_provider(
        provider_npi=claim_payload.provider_npi, net_fees_for_claim=net_fees, db=db
    )

    claim_details = claim_payload.dict()
    claim_details["claim_id"] = claim_id
    claim_details["net_fees"] = net_fees
    call_payments(claim_details=ClaimDetails.parse_obj(claim_details))

    return claim_details
