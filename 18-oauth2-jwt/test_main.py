from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_login_token_and_protected_route():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    token = data["access_token"]
    protected = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert protected.status_code == 200, protected.text
    assert protected.json()["Username"] == "admin"
