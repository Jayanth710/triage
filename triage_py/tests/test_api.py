from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "strategies" in r.json()

def test_triage_rules_billing():
    r = client.post("/triage", json={"id":"1","text":"I was charged twice for my order #A12345"})
    assert r.status_code == 200
    data = r.json()
    assert "department" in data and "confidence" in data and "strategy" in data and "draft" in data

def test_validation_error():
    r = client.post("/triage", json={"id":"2"})  # missing text
    assert r.status_code == 422