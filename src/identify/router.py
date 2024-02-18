from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .deps import get_db


router = APIRouter()


@router.post("/identify")
def identify(db: Session=Depends(get_db)):
    pass