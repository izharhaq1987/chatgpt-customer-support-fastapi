from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index():
    r = client.get("/")
    assert r.status_code == 200
    assert "Mock Zendesk" in r.text or "running" in r.text

def test_create_and_get_ticket():
    payload = {
        "subject": "Refund inquiry",
        "description": "Refund my recent purchase",
        "requester_email": "user@example.com",
        "priority": "high"
    }
    r = client.post("/tickets/", json = payload)
    assert r.status_code == 200
    tid = r.json()["id"]

    r2 = client.get(f"/tickets/{tid}")
    assert r2.status_code == 200
    assert r2.json()["subject"] == "Refund inquiry"
