from sqlalchemy.orm import Session

from app.database import models


def top_ten_fee_generating_providers(db: Session):
    """Returns providers in descending order of provider fees

    Args:
        db (Session): database sessions

    Returns:
        List[models.AgregateProviderFees]: Provider info
    """
    return (
        db.query(models.AgregateProviderFees)
        .order_by(models.AgregateProviderFees.aggregate_net_fees.desc())
        .limit(10)
        .all()
    )
