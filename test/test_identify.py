from fastapi.testclient import TestClient
from src.main import app
from src.db import Base, engine, SessionLocal
from src.identify.model import Contact, LinkPrecedence


class TestIdentify:
    _url = '/identify'

    client = TestClient(app)

    @classmethod
    def setup_class(cls):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def setup_method(self):
        self.session = SessionLocal()
    
    def teardown_method(self):
        self.session.rollback()
        self.session.close()
        
    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(engine)


    def test_identify_primary(self):
        new_contact = Contact(email="lorraine@hillvalley.edu", phonenumber="123456", linkprecedence=LinkPrecedence.PRIMARY)
        self.session.add(new_contact)
        self.session.commit()

        _request = {"email": "lorraine@hillvalley.edu", "phoneNumber":123456}
        contact_response = self.client.post(url=self._url, json=_request)

        contact_response_json = contact_response.json()
        assert contact_response_json["primaryContactId"] == new_contact.id
        assert contact_response_json["emails"] == [new_contact.email]
        assert contact_response_json["phoneNumbers"] == [new_contact.phonenumber]


    # def test_identify_secondary_with_email(self):
    #     pass

    # def test_identify_secondary_with_phoneNumber():
    #     pass

    # def test_identify_create_new_primary():
    #     pass

    # def test_identify_create_new_secondary():
    #     pass

    # def test_identify_create_convert_primary_to_secondary():
    #     pass