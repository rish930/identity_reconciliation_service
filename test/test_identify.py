from fastapi.testclient import TestClient
from src.main import app

_url = '/identify'

client = TestClient(app)

def setup():
    pass

def test_identify_200():
    pass