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

    class json_schema_extra:
        schema_extra = {
            "example": 	{
                "contact":{
                    "primaryContatctId": 11,
                    "emails": ["george@hillvalley.edu","biffsucks@hillvalley.edu"],
                    "phoneNumbers": ["919191","717171"],
                    "secondaryContactIds": [27]
                }
	        }
        }