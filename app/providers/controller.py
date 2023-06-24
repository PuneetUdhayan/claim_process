from sqlalchemy.orm import Session

from app.providers import transaction


def top_ten_fee_generating_providers(db: Session):
    return transaction.top_ten_fee_generating_providers(db=db)
