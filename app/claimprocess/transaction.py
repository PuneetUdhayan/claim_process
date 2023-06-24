from datetime import datetime

from sqlalchemy.orm import Session

from app.database import models


def create_claim(
    claim_id: str,
    service_date: datetime,
    submitted_procedure: str,
    plan_group_number: str,
    subscriber_number: str,
    provider_npi: int,
    currency: str,
    provider_fees: float,
    allowed_fees: float,
    member_coinsurance: float,
    member_copay: float,
    net_fees: float,
    db: Session,
):
    db.add(
        models.Claim(
            id=claim_id,
            service_date=service_date,
            submitted_procedure=submitted_procedure,
            plan_group_number=plan_group_number,
            subscriber_number=subscriber_number,
            provider_npi=provider_npi,
            currency=currency,
            provider_fees=provider_fees,
            allowed_fees=allowed_fees,
            member_coinsurance=member_coinsurance,
            member_copay=member_copay,
            net_fees=net_fees,
        )
    )


def increment_net_fee_for_provider(
    provider_npi: int, net_fees_for_claim: float, db: Session
):
    net_fees = (
        db.query(models.AgregateProviderFees)
        .where(models.AgregateProviderFees.provider_npi == provider_npi)
        .first()
    )
    if net_fees:
        net_fees.aggregate_net_fees += net_fees_for_claim
    else:
        net_fees = models.AgregateProviderFees(
            provider_npi=provider_npi, aggregate_net_fees=net_fees_for_claim
        )
        db.add(net_fees)
