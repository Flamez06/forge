from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)

# def test_create_application():
#     for i in range(1,4):
#         response = client.post(
#                 "/applications",
#                 json={
#                     "name": f"Test App {i}",
#                     "repository_url": f"https://github.com/test/repo{i}"
#                 }
#             )
        
#         assert response.status_code == 200
        
#         data = response.json()
        
#         assert data["name"] == f"Test App {i}"
#         assert data["repository_url"] == f"https://github.com/test/repo{i}"
#         assert "id" in data

def test_application():
    response = client.post(
            "/applications",
            json={
                "name": "Test App",
                "repository_url": "https://github.com/test/repo"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test App"
    assert data["repository_url"] == "https://github.com/test/repo"
    assert "id" in data
    
    client.delete(f"/applications/{data['id']}")