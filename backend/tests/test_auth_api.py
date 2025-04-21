import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db
from app.models import User
from app.utils import auth_utils  

client = TestClient(app)
def test_password_hashing():
    raw_password = "test123"
    hashed = auth_utils.hash_password(raw_password)
    assert auth_utils.verify_password(raw_password, hashed)



# def create_test_user(db: Session, email: str, password: str):
#     user = User(
#         username="testuser",
#         email=email,
#         password=hash_password(password),
#         full_name="Test User",
#         address="123 Street",
#         phone="1234567890",
#         role="customer",
#         is_verified=True
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


@pytest.fixture
def override_get_db(test_db):
    def _override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = _override_get_db


# def test_register_user(override_get_db):
#     response = client.post(
#         "/register",
#         json={
#             "username": "newuser",
#             "email": "newuser@example.com",
#             "password": "securepass",
#             "full_name": "New User",
#             "address": "Somewhere",
#             "phone": "0123456789",
#             "role": "customer"
#         },
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"


def test_login_user(override_get_db, test_db):
    create_test_user(test_db, "loginuser@example.com", "mypassword")

    response = client.post(
        "/login",
        json={"email": "loginuser@example.com", "password": "mypassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"