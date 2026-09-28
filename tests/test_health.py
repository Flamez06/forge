from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    # Raise error if the result of the statement is not true.
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
def test_redis():
    response = client.get("/redis-test")
    assert response.status_code == 200
    assert response.json() == {"redis": "hello"}