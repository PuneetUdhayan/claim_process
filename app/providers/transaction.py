from sqlalchemy.orm import Session

from app.database import models


def top_ten_fee_generating_providers(db: Session):
    return (
        db.query(models.AgregateProviderFees)
        .order_by(models.AgregateProviderFees.aggregate_net_fees.desc())
        .limit(10)
        .all()
    )
