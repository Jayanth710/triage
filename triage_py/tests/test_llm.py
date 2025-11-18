import types, asyncio
from fastapi.testclient import TestClient
import api.main as api_main
from core.models import RouteDecision

client = TestClient(api_main.app)

async def fake_decide(ticket):
    return RouteDecision(department="Billing", confidence=0.99, strategy="fake")

def test_triage_with_fake_orchestrator(monkeypatch):
    monkeypatch.setattr(api_main.orchestrator, "decide", fake_decide)
    r = client.post("/triage", json={"id":"9","text":"anything"})
    assert r.status_code == 200
    data = r.json()
    assert data["department"] == "Billing"
    assert data["strategy"] == "fake"