from fastapi.testclient import TestClient
from src.main import app

_url = '/identify'

client = TestClient(app)

def setup():
    pass

def test_identify_primary():
    _request = {"email": "lorraine@hillvalley.edu", "phoneNumber":123456}
    contact_response = client.post(url=_url, json=_request)

    contact_response_json = contact_response.json()
    assert contact_response_json["primaryContactId"] == 1
    assert contact_response_json["emails"] == [_request["email"]]
    assert contact_response_json["phoneNumbers"] == [str(_request["phoneNumber"])]


# def test_identify_secondary_with_email():
#     pass

# def test_identify_secondary_with_phoneNumber():
#     pass

# def test_identify_create_new_primary():
#     pass

# def test_identify_create_new_secondary():
#     pass

# def test_identify_create_convert_primary_to_secondary():
#     pass