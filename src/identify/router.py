from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schema import IdentifyRequest
from .service import get_consolidated_contact

from .deps import get_db


router = APIRouter()


@router.post("/identify")
def identify(request_body: IdentifyRequest, db: Session=Depends(get_db)):
    contacts = get_consolidated_contact(email=request_body.email,
                                        phoneNumber=request_body.phoneNumber,
                                        db=db)
    return contacts