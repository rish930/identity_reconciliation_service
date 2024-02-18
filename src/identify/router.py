from fastapi import APIRouter


router = APIRouter()


@router.post("/identify")
def identify():
    pass