from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schema import IdentifyRequest, IdentifyResponse
from .service import get_consolidated_contact

from .deps import get_db


router = APIRouter()


@router.post("/identify", response_model=IdentifyResponse)
def identify(request_body: IdentifyRequest, db: Session = Depends(get_db)):
    if request_body.email is None and request_body.phoneNumber is None:
        raise HTTPException(
            status_code=400,
            detail="Atleast one of email and phoneNumber should be given",
        )

    contacts = get_consolidated_contact(
        email=request_body.email, phone_number=request_body.phoneNumber, db=db
    )
    
    return {"contact": contacts}
