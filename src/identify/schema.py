from pydantic import BaseModel, EmailStr
from typing import List, Optional


class IdentifyRequest(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[int] = None


class ContactDetails(BaseModel):
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]


class IdentifyResponse(BaseModel):
    contact: ContactDetails
