from fastapi.testclient import TestClient

from backend.api import app


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert "model_loaded" in data


def test_predict_endpoint():
    sample_payload = {
        "checking_status": "0-to-200",
        "duration_months": 24,
        "credit_history": "existing-paid",
        "purpose": "radio-tv",
        "credit_amount": 3500.0,
        "savings": "100-to-500",
        "employment": "1-to-4",
        "installment_rate": 2,
        "personal_status": "male-single",
        "other_debtors": "none",
        "residence_years": 3,
        "property": "real-estate",
        "age": 32,
        "other_installment_plans": "none",
        "housing": "own",
        "existing_credits": 1,
        "job": "skilled-employee",
        "dependents": 1,
        "telephone": "yes",
        "foreign_worker": "yes",
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=sample_payload)

    print("Status:", response.status_code)
    print("Body:", response.text)

    assert response.status_code == 200
    data = response.json()

    assert data["prediction"] in ["good", "high-risk"]
    assert 300 <= data["simulated_credit_score"] <= 850