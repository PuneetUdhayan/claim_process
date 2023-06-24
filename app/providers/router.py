from typing import List

from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, Depends, status, HTTPException

from app.database import get_db
from app.schema import StandardResponse
from app.providers import controller
from app.authentication.api_key import validate_api_key

router = APIRouter(
    prefix="/providers", tags=["Providers"], dependencies=[Depends(validate_api_key)]
)


@router.get("/top-ten", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def top_ten_providers(db: Session = Depends(get_db)):
    """Returns top 10 providers by net fees

    Args:
        db (Session, optional): database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: Thrown when an unforeseen error occurs

    Returns:
        StandardResponse
    """
    try:
        data = controller.top_ten_fee_generating_providers(db=db)
        return StandardResponse(status=True, data=data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
