from fastapi.testclient import TestClient
from src.main import app


_url = "/"
client = TestClient(app)


def test_health():
    response = client.get("/")
    assert response.status_code == 200
