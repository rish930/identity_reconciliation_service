from sqlalchemy.orm import Session
from .model import Contact, LinkPrecedence
from typing import List
from .schema import ContactDetails
import logging

logging.getLogger().setLevel(logging.INFO)


def get_consolidated_contact(
    email: str, phone_number: int, db: Session
) -> ContactDetails:
    if phone_number is not None:
        phone_number = str(phone_number)
    if email is not None:
        email = str(email)

    contact = is_contact_exists(email=email, phone_number=phone_number, db=db)
    if contact is not None:
        logging.info("Record with same email and phonenumber exists")
        if contact.linkprecedence == LinkPrecedence.PRIMARY:
            primary = contact
            db.commit()
            out = consolidate(primary, [])
            return out
        else:
            primary = get_contact_by_id(id=contact.linkedid, db=db)
    else:
        logging.info("Contact does not exists")
        primary_contacts = get_primary_contacts(
            email=email, phone_number=phone_number, db=db
        )
        if len(primary_contacts) == 0:
            logging.info("Creating new primary")
            primary = Contact(
                email=email,
                phonenumber=phone_number,
                linkprecedence=LinkPrecedence.PRIMARY,
            )
            db.add(primary)

        elif len(primary_contacts) == 1:
            logging.info("Primary exists")
            primary = primary_contacts[0]
            if email is not None and phone_number is not None:
                logging.info("Creating new secondary")
                new_contact = Contact(
                    email=email,
                    phonenumber=phone_number,
                    linkedid=primary.id,
                    linkprecedence=LinkPrecedence.SECONDARY,
                )
                db.add(new_contact)

        elif len(primary_contacts) == 2:
            logging.info("Multiple Primary, converting one to secondary")
            primary = primary_contacts[0]
            primary2 = primary_contacts[1]
            primary2.linkedid = primary.id
            primary2.linkprecedence = LinkPrecedence.SECONDARY
            
            update_secondary_contacts(
                linkedid=primary2.id, new_linkedid=primary.id, db=db
            )

        else:
            raise Exception(
                "Something wrong with db, more than 2 primary contacts found!"
            )

    db.commit()

    secondary_contacts = get_all_secondary_contacts(
        primary_contact_id=primary.id, db=db
    )

    consolidated_contacts = consolidate(primary, secondary_contacts)
    logging.info("Returning consolidated from service")
    return consolidated_contacts


def get_all_secondary_contacts(primary_contact_id: int, db: Session) -> List[Contact]:
    secondary_contacts = (
        db.query(Contact)
        .filter(Contact.linkedid == primary_contact_id)
        .order_by(Contact.id)
        .all()
    )

    return secondary_contacts


def consolidate(primary_contact, secondary_contacts: List[Contact]) -> ContactDetails:

    out = ContactDetails(
        **{
            "primaryContactId": primary_contact.id,
            "emails": [],
            "phoneNumbers": [],
            "secondaryContactIds": [],
        }
    )

    primary_email = primary_contact.email
    primary_phoneNumber = primary_contact.phonenumber

    email_done = set()
    phone_number_done = set()

    if primary_email is not None:
        if primary_email not in email_done:
            out.emails.append(primary_email)
            email_done.add(primary_email)

    if primary_phoneNumber is not None:
        if primary_phoneNumber not in phone_number_done:
            out.phoneNumbers.append(primary_phoneNumber)
            phone_number_done.add(primary_phoneNumber)

    for contact in secondary_contacts:
        email = contact.email
        phone_number = contact.phonenumber
        if email is not None and email not in email_done:
            out.emails.append(email)
            email_done.add(email)
        if phone_number is not None and phone_number not in phone_number_done:
            out.phoneNumbers.append(contact.phonenumber)
            phone_number_done.add(phone_number)

        out.secondaryContactIds.append(contact.id)
    logging.info("Consolidated")
    return out


def is_contact_exists(email: str, phone_number: str, db: Session) -> Contact:

    query = db.query(Contact).filter(
        Contact.email == email, Contact.phonenumber == phone_number
    )
    contact = query.first()
    return contact


def get_contact_by_id(id: int, db: Session) -> Contact:
    return db.query(Contact).filter_by(id=id).first()


def get_primary_contacts(email: str, phone_number: str, db: Session) -> List[Contact]:
    """
    returns list of unique primary contacts sorted in ascending order w.r.t id
    """
    logging.info("Getting primary contacts")
    contacts = []
    if phone_number is not None:
        contact1 = db.query(Contact).filter(Contact.phonenumber == phone_number).first()
        contact1 = get_oldest_primary_contact(contact=contact1, db=db)
        if contact1:
            contacts.append(contact1)
    if email is not None:
        contact2 = db.query(Contact).filter(Contact.email == email).first()
        contact2 = get_oldest_primary_contact(contact=contact2, db=db)
        if contact2:
            contacts.append(contact2)

    if len(contacts) > 1:
        contacts.sort(key=lambda x: x.id)
    return contacts


def get_oldest_primary_contact(contact: Contact, db: Session) -> Contact:
    if contact is not None:
        if contact.linkprecedence == LinkPrecedence.PRIMARY:
            return contact
        else:
            contact1 = get_contact_by_id(contact.linkedid, db)
            return contact1
    else:
        return None


def update_secondary_contacts(linkedid: int, new_linkedid: int, db: Session) -> None:
    db.query(Contact).filter(Contact.linkedid == linkedid).update(
        {Contact.linkedid: new_linkedid}
    )
