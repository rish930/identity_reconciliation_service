from fastapi.testclient import TestClient
from src.main import app
from src.db import Base, engine, SessionLocal
from src.identify.model import Contact, LinkPrecedence
import pytest


class TestIdentify:
    _url = "/identify"

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
    def primary_contact(self):
        new_contact = Contact(
            email="lorraine@hillvalley.edu",
            phonenumber="123456",
            linkprecedence=LinkPrecedence.PRIMARY,
        )
        self.session.add(new_contact)
        self.session.commit()
        self.primary_contact = new_contact
        return new_contact

    @pytest.fixture
    def secondary_contact(self, primary_contact):
        new_contact = Contact(
            email="mcfly@hillvalley.edu",
            phonenumber="123456",
            linkprecedence=LinkPrecedence.SECONDARY,
            linkedid=primary_contact.id,
        )
        self.session.add(new_contact)
        self.session.commit()
        return new_contact

    def test_identify_primary(self, primary_contact):
        _request = {"email": "lorraine@hillvalley.edu", "phoneNumber": 123456}
        contact_response = self.client.post(url=self._url, json=_request)

        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == primary_contact.id
        assert contact_response_json["emails"] == [primary_contact.email]
        assert contact_response_json["phoneNumbers"] == [primary_contact.phonenumber]
        assert contact_response_json["secondaryContactIds"] == []

    def test_identify_secondary(self, secondary_contact):
        _request = {"email": "mcfly@hillvalley.edu", "phoneNumber": 123456}
        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == self.primary_contact.id
        assert contact_response_json["emails"] == [
            self.primary_contact.email,
            secondary_contact.email,
        ]
        assert contact_response_json["phoneNumbers"] == [secondary_contact.phonenumber]
        assert contact_response_json["secondaryContactIds"] == [secondary_contact.id]

    def test_identify_secondary_email_null(self, secondary_contact):
        _request = {"email": None, "phoneNumber": 123456}
        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == self.primary_contact.id
        assert contact_response_json["emails"] == [
            self.primary_contact.email,
            secondary_contact.email,
        ]
        assert contact_response_json["phoneNumbers"] == [
            self.primary_contact.phonenumber
        ]
        assert contact_response_json["secondaryContactIds"] == [secondary_contact.id]

    def test_identify_secondary_number_null(self, secondary_contact):
        _request = {"email": "mcfly@hillvalley.edu", "phoneNumber": None}
        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == self.primary_contact.id
        assert contact_response_json["emails"] == [
            self.primary_contact.email,
            secondary_contact.email,
        ]
        assert contact_response_json["phoneNumbers"] == [
            self.primary_contact.phonenumber
        ]
        assert contact_response_json["secondaryContactIds"] == [secondary_contact.id]

    def test_identify_create_new_primary(self):
        _request = {"email": None, "phoneNumber": 123456}
        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == 1
        assert contact_response_json["emails"] == []
        assert contact_response_json["phoneNumbers"] == [str(_request["phoneNumber"])]
        assert contact_response_json["secondaryContactIds"] == []

    def test_identify_create_new_secondary(self, primary_contact):
        _request = {"email": "something@hey.com", "phoneNumber": 123456}
        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == 1
        assert contact_response_json["emails"] == [
            primary_contact.email,
            _request["email"],
        ]
        assert contact_response_json["phoneNumbers"] == [primary_contact.phonenumber]
        assert contact_response_json["secondaryContactIds"] == [2]

    def test_identify_create_convert_primary_to_secondary(self, primary_contact):
        second_primary = Contact(
            email="secondprimary@hey.com",
            phonenumber="789123",
            linkprecedence=LinkPrecedence.PRIMARY,
        )
        self.session.add(second_primary)
        self.session.commit()

        _request = {
            "email": second_primary.email,
            "phoneNumber": int(primary_contact.phonenumber),
        }
        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == 1
        assert contact_response_json["emails"] == [
            primary_contact.email,
            second_primary.email,
        ]
        assert contact_response_json["phoneNumbers"] == [
            primary_contact.phonenumber,
            second_primary.phonenumber,
        ]
        assert contact_response_json["secondaryContactIds"] == [second_primary.id]

        self.session.refresh(second_primary)
        assert second_primary.linkprecedence == LinkPrecedence.SECONDARY
        assert second_primary.linkedid == primary_contact.id

    def test_identify_email_null_phonenumber_null(self):
        _request = {"email": None, "phoneNumber": None}
        contact_response = self.client.post(url=self._url, json=_request)

        assert contact_response.status_code == 400

    @pytest.mark.parametrize(
        "email", ["john.doe@examplecom", "johnexample.com", "john"]
    )
    def test_invalid_email_failure(self, email):
        _request = {"email": email, "phoneNumber": 1233}

        respone = self.client.post(url=self._url, json=_request)

        assert respone.status_code == 422

    def test_identify_create_convert_primary_to_secondary_update_all_secondary(
        self, secondary_contact
    ):
        second_primary = Contact(
            email="secondprimary@hey.com",
            phonenumber="789123",
            linkprecedence=LinkPrecedence.PRIMARY,
        )
        self.session.add(second_primary)
        self.session.commit()
        secondary_contact.linkedid = second_primary.id
        self.session.commit()

        self.session.refresh(second_primary)
        _request = {
            "email": self.primary_contact.email,
            "phoneNumber": second_primary.phonenumber,
        }

        contact_response = self.client.post(url=self._url, json=_request)
        contact_response_json = contact_response.json()["contact"]
        assert contact_response_json["primaryContactId"] == 1
        assert contact_response_json["emails"] == [
            self.primary_contact.email,
            secondary_contact.email,
            second_primary.email,
        ]
        assert contact_response_json["phoneNumbers"] == [
            self.primary_contact.phonenumber,
            second_primary.phonenumber,
        ]
        assert contact_response_json["secondaryContactIds"] == [
            secondary_contact.id,
            second_primary.id,
        ]
