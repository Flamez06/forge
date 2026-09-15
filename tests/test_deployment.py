from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_create_deployment():
    application = client.post(
        "/applications",
        json={
            "name": "Deploy Test",
            "repository_url": "https://github.com/test/repo"
        }
    )

    assert application.status_code == 200

    application_id = application.json()["id"]

    response = client.post(
        f"/deployments/{application_id}/deploy",
        json={"commit_sha": "3a82889"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["application_id"] == application_id
    assert data["commit_sha"] == "3a82889"
    
    client.delete(f"/deployments/{data['id']}")
    client.delete(f"/applications/{application_id}")
   