from src.db import Base
from sqlalchemy import Column

from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, UniqueConstraint
import enum
from sqlalchemy.sql import func


class LinkPrecedence(enum.Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    phonenumber = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linkedid = Column(Integer, ForeignKey("contact.id"), nullable=True)
    linkprecedence = Column(Enum(LinkPrecedence), nullable=True)
    create_date = Column(DateTime, nullable=False, server_default=func.now())
    update_date = Column(DateTime, nullable=True, onupdate=func.now())
    delete_date = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("email", "phonenumber", name="uix_email_phonenumber_1"),
    )


class ContactPrimary(Base):
    __tablename__ = "contact_primary"
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey(Contact.id, name="fk_contact_secondary_id"))
    primary_id = Column(Integer, ForeignKey(Contact.id, name="fk_contact_primary_id"))
