from src.db import Base
from sqlalchemy import Column

from sqlalchemy import Integer, String, Enum, TIMESTAMP, DateTime
from enum import Enum

class LinkPrecedence(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Contact(Base):
    __tablename__ = "Contact"

    id = Column(Integer, primary_key=True)
    phoneNumber = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linkedId =  Column(Integer, nullable=True) # TODO should be FK in same table
    linkPrecedence =  Column(Enum(LinkPrecedence), default=LinkPrecedence.PRIMARY)
    createdAt = Column(DateTime, nullable=False) # TODO replace with default timestamp
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)
