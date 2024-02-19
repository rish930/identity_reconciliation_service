from fastapi.testclient import TestClient
from src.main import app
from src.db import Base, engine, SessionLocal
from src.identify.model import Contact, LinkPrecedence
import pytest


class TestIdentify:
    _url = '/identify'

    client = TestClient(app)

    def setup_method(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = SessionLocal()
    
    def teardown_method(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(engine)


    @pytest.fixture
    def new_primary_contact(self):
        new_contact = Contact(email="lorraine@hillvalley.edu", phonenumber="123456", linkprecedence=LinkPrecedence.PRIMARY)
        self.session.add(new_contact)
        self.session.commit()
        self.primary_contact = new_contact
        return new_contact
    
    @pytest.fixture
    def new_secondary_contact(self, new_primary_contact):
        new_contact = Contact(email="mcfly@hillvalley.edu", phonenumber="123456", linkprecedence=LinkPrecedence.SECONDARY, linkedid=new_primary_contact.id)
        self.session.add(new_contact)
        self.session.commit()
        return new_contact

    def test_identify_primary(self, new_primary_contact):
        _request = {"email": "lorraine@hillvalley.edu", "phoneNumber":123456}
        contact_response = self.client.post(url=self._url, json=_request)

        contact_response_json = contact_response.json()
        assert contact_response_json["primaryContactId"] == new_primary_contact.id
        assert contact_response_json["emails"] == [new_primary_contact.email]
        assert contact_response_json["phoneNumbers"] == [new_primary_contact.phonenumber]


    def test_identify_secondary_with_email(self, new_secondary_contact):
        _request = {"email": "mcfly@hillvalley.edu", "phoneNumber":123456}
        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()
        assert contact_response_json["primaryContactId"] == self.primary_contact.id
        assert contact_response_json["emails"] == [self.primary_contact.email, new_secondary_contact.email]
        assert contact_response_json["phoneNumbers"] == [new_secondary_contact.phonenumber]


    # def test_identify_secondary_with_phoneNumber():
    #     pass

    # def test_identify_create_new_primary():
    #     pass

    # def test_identify_create_new_secondary():
    #     pass

    # def test_identify_create_convert_primary_to_secondary():
    #     pass