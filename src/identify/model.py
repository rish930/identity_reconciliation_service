from src.db import Base
from sqlalchemy import Column

from sqlalchemy import Integer, String, Enum, TIMESTAMP, DateTime, ForeignKey
from enum import Enum

class LinkPrecedence(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    phonenumber = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linkedid =  Column(Integer, nullable=True) # TODO should be FK in same table
    linkprecedence =  Column(String, nullable=True)
    createdat = Column(DateTime, nullable=False) # TODO replace with default timestamp
    updatedat = Column(DateTime, nullable=True)
    deletedat = Column(DateTime, nullable=True)

    # TODO add uniqueness constraint to (email, phonenumber)


class ContactPrimary(Base):
    __tablename__ = "contact_primary"
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey(Contact.id, name="fk_contact_secondary_id"))
    primary_id = Column(Integer, ForeignKey(Contact.id, name="fk_contact_primary_id"))