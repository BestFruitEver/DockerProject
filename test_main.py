from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_post_create():
    response = client.get("/create/")
    assert response.status_code == 200
    