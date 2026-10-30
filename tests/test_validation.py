"""Tests for MedBot Input Validation and Error Handling."""

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ask_empty_payload():
    """Verify empty POST payload returns 422 Unprocessable Entity."""
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ask_short_question():
    """Verify question below 5 characters is rejected with 422."""
    response = client.post("/ask", json={"question": "doc?"})
    assert response.status_code == 422


def test_ask_whitespace_only():
    """Verify question containing only whitespace is rejected with 422."""
    response = client.post("/ask", json={"question": "          "})
    assert response.status_code == 422


def test_ask_missing_api_key(monkeypatch):
    """Verify 503 Service Unavailable when API key is unconfigured."""
    monkeypatch.setattr("app.config.GROQ_API_KEY", "")
    monkeypatch.setattr("app.config.GEMINI_API_KEY", "")
    response = client.post("/ask", json={"question": "What is normal blood pressure?"})
    assert response.status_code == 503
    data = response.json()
    assert "API key is not configured" in data["detail"]


def test_ask_success_with_mocked_workflow(monkeypatch):
    """Verify successful response formatting when LLM and medical workflow return an answer."""
    monkeypatch.setattr("app.config.GROQ_API_KEY", "mock_valid_key_123")
    monkeypatch.setattr("app.config.GEMINI_API_KEY", "mock_valid_key_123")

    mock_result = {
        "answer": "Normal resting blood pressure is defined as systolic < 120 mmHg and diastolic < 80 mmHg.",
        "sources": ["Cardiovascular Health & Hypertension Clinical Guidelines"],
    }

    with patch("app.main.run_medical_workflow", return_value=mock_result):
        response = client.post(
            "/ask",
            json={"question": "What are the blood pressure thresholds for hypertension?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "120 mmHg" in data["answer"]
        assert "Cardiovascular Health & Hypertension Clinical Guidelines" in data["sources"]
        assert "Disclaimer:" in data["disclaimer"]
