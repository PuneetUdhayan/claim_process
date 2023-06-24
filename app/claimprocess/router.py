from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

from app.database import get_db
from app.schema import StandardResponse
from app.dependencies import db_session_handler
from app.claimprocess.schemas import ClaimPayload
from app.claimprocess.controller import claim_process
from app.authentication.api_key import validate_api_key


router = APIRouter(
    prefix="/claim", tags=["Process claim"], dependencies=[Depends(validate_api_key)]
)


@router.post("")
def process_claim(claim_payload: ClaimPayload, db: Session = Depends(get_db)):
    """Endpoint to process claims.

    Args:
        claim_payload (ClaimPayload): Details of the claim
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: Thrown when an unforeseen error occurs

    Returns:
        StandardResponse
    """
    try:
        claim_details = db_session_handler(
            claim_process, {"claim_payload": claim_payload, "db": db}, db=db
        )
        return StandardResponse(status=True, data=claim_details)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
