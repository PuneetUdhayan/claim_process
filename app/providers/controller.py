from sqlalchemy.orm import Session

from app.providers import transaction


def top_ten_fee_generating_providers(db: Session):
    """Returns top 10 

    Args:
        db (Session): database session

    Returns:
        List[models.AgregateProviderFees]: Provider info
    """
    return transaction.top_ten_fee_generating_providers(count=10, db=db)
