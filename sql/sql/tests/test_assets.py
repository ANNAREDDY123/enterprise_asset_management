from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_api():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Enterprise Asset Management API is running"

def test_register_user():
    response = client.post(
        "/register",
        json={
            "username": "admin_test",
            "password": "admin123",
            "role": "Admin"
        }
    )
    assert response.status_code in [200, 400]
