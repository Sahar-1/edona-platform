from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """
    Vérifie que la route de santé /health répond avec un statut 200
    et renvoie {"status": "ok"}.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"

def test_health_check_structure():
    """
    Vérifie la présence de la clé status dans la réponse du healthcheck.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()