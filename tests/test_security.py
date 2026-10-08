import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
os.environ["API_SECURITY_KEY"] = "test-security-key"

from backend.main import app, client as openai_client
from rate_limiter import reset_rate_limiter


@pytest.fixture(autouse=True)
def reset_limiter():
    reset_rate_limiter()
    yield
    reset_rate_limiter()


@pytest.fixture
def api_client(monkeypatch):
    def fake_create(**kwargs):
        class Message:
            content = "Test AI response"

        class Choice:
            message = Message()

        class Response:
            choices = [Choice()]

        return Response()

    monkeypatch.setattr(
        openai_client.chat.completions,
        "create",
        fake_create,
    )
    return TestClient(app)


def test_health_is_public(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_is_public(api_client):
    response = api_client.get("/")
    assert response.status_code == 200


def test_generate_without_api_key_returns_401(api_client):
    response = api_client.post("/generate", json={"prompt": "Hello"})
    assert response.status_code == 401


def test_generate_with_invalid_api_key_returns_401(api_client):
    response = api_client.post(
        "/generate",
        headers={"X-API-Key": "wrong-key"},
        json={"prompt": "Hello"},
    )
    assert response.status_code == 401


def test_generate_with_valid_api_key_succeeds(api_client):
    response = api_client.post(
        "/generate",
        headers={"X-API-Key": "test-security-key"},
        json={"prompt": "Hello"},
    )
    assert response.status_code == 200
    assert response.json()["response"] == "Test AI response"


def test_feedback_requires_api_key(api_client):
    payload = {
        "prompt": "Hello",
        "response": "World",
        "rating": "positive",
        "comment": "",
    }
    response = api_client.post("/feedback", json=payload)
    assert response.status_code == 401


def test_feedback_stats_requires_api_key(api_client):
    response = api_client.get("/feedback/stats")
    assert response.status_code == 401


def test_generate_rate_limit_returns_429(api_client):
    headers = {"X-API-Key": "test-security-key"}

    for _ in range(10):
        response = api_client.post(
            "/generate",
            headers=headers,
            json={"prompt": "Hello"},
        )
        assert response.status_code == 200

    response = api_client.post(
        "/generate",
        headers=headers,
        json={"prompt": "Hello"},
    )

    assert response.status_code == 429
    assert "Retry-After" in response.headers
