from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_submit_positive_feedback():
    response = client.post("/feedback", json={
        "prompt": "What is RAG?",
        "response": "RAG combines retrieval with generation.",
        "rating": "positive",
        "comment": "Clear explanation"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Feedback submitted successfully"

def test_invalid_rating():
    response = client.post("/feedback", json={
        "prompt": "What is RAG?",
        "response": "A response",
        "rating": "invalid",
        "comment": ""
    })
    assert response.status_code == 400

def test_feedback_stats():
    response = client.get("/feedback/stats")
    assert response.status_code == 200
    assert "total_feedback" in response.json()
