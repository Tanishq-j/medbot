"""Tests for MedBot Health and Frontend Endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify /health returns 200 and lists all 3 Agno medical agents."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "MedBot" in data["app_name"]
    assert "model" in data
    assert isinstance(data["groq_configured"], bool)

    agents = data["agents"]
    assert len(agents) == 3
    assert "Medical Query Analyzer" in agents
    assert "Medical Research Agent" in agents
    assert "Medical Answer Reviewer" in agents


def test_root_serves_frontend():
    """Verify GET / returns 200 and serves HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "MedBot" in response.text
    assert "Medical Query Analyzer" in response.text
