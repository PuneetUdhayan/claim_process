from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.claimprocess.schemas import ClaimPayload
from app.authentication.api_key import validate_api_key


router = APIRouter(
    prefix="/claim",
    tags=['Process claim'],
    dependencies=[Depends(validate_api_key)]
)


@router.post('')
def process_claim(claim_payload: ClaimPayload,db: Session = Depends(get_db)):
    print(claim_payload)
    pass
