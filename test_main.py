from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_audit_approved_transaction():
    payload = {
        "account_id": "ACC-88392",
        "amount": 250.50,
        "currency": "USD",
        "timestamp": "2026-10-27T14:30:00Z",
        "merchant_category": "groceries",
    }
    response = client.post("/audit", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "APPROVED"
    assert data["risk_score"] == 0
    assert data["reasons"] == []


def test_audit_flagged_transaction():
    payload = {
        "account_id": "ACC-99211",
        "amount": 15000.00,
        "currency": "USD",
        "timestamp": "2026-10-27T02:15:00Z",
        "merchant_category": "crypto_exchange",
    }
    response = client.post("/audit", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "FLAGGED"
    assert data["risk_score"] == 100
    assert "High value transaction alert (> 10,000 currency units)" in data["reasons"]


def test_invalid_amount_is_rejected():
    payload = {
        "account_id": "ACC-1",
        "amount": -1,
        "currency": "USD",
        "timestamp": "2026-10-27T14:30:00Z",
        "merchant_category": "groceries",
    }
    response = client.post("/audit", json=payload)
    assert response.status_code == 422
