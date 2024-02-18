from pydantic import BaseModel
from typing import List


class IdentifyRequest(BaseModel):
    email: str
    phoneNumber: int


class ContactDetails(BaseModel):
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]


class IdentifyResponse(BaseModel):
    contact: ContactDetails
