from sqlalchemy.orm import Session
from .model import Contact, LinkPrecedence
from typing import List
from .schema import ContactDetails
import logging


def get_consolidated_contact(email: str, phoneNumber: str, db: Session):
    # check if contact exists
        # email and phoneNumber
    contact = is_contact_exists(email=email, 
                                 phoneNumber=phoneNumber, 
                                 db=db)
    
    if contact.linkprecedence==LinkPrecedence.PRIMARY:
        primary = contact
    else:
        primary = get_contact_by_id(id=contact.linkedid, db=db)
    
    secondary_contacts = get_all_secondary_contacts(primary_contact_id=primary.id, db=db)

    consolidated_contacts = consolidate(primary, secondary_contacts)
    
    return consolidated_contacts

def get_all_secondary_contacts(primary_contact_id: int, db: Session):
    secondary_contacts = db.query(Contact).filter(Contact.linkedid==primary_contact_id).all()

    return secondary_contacts

def consolidate(primary_contact, secondary_contacts: List[Contact]):
    
    out = ContactDetails(**{"primaryContactId": primary_contact.id,
     "emails":[],
     "phoneNumbers": [],
     "secondaryContactIds": []})
    
    primary_email = primary_contact.email
    primary_phoneNumber = primary_contact.phonenumber

    email_done = set()
    phone_number_done = set()

    if primary_email!=None:
        if primary_email not in email_done:
            out.emails.append(primary_email)
            email_done.add(primary_email)

    if primary_phoneNumber!=None:
        if primary_phoneNumber not in phone_number_done:
            out.phoneNumbers.append(primary_phoneNumber)
            phone_number_done.add(primary_phoneNumber)

    for contact in secondary_contacts:
        email = contact.email
        phone_number = contact.phonenumber
        if email!=None and email not in email_done:
            out.emails.append(email)
            email_done.add(email)
        if phone_number!=None and phone_number not in phone_number_done:
            out.phoneNumbers.append(contact.phonenumber)
            phone_number_done.add(phone_number)
    
    return out


def is_contact_exists(email: str, phoneNumber: str, db: Session):
    
    query = db.query(Contact).filter(Contact.email == email, Contact.phonenumber==str(phoneNumber))
    contacts = query.first()
    return contacts


def get_contact_by_id(id: int, db: Session):
    logging.info("get_contact_by_id..........")
    return db.query(Contact).filter_by(id=id).first()