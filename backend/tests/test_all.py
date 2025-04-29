import pytest
from fastapi import status
from unittest.mock import Mock, patch
from app.models import User

# 1. Auth Endpoints -----------------------------------------------------------
def test_register(client, db_session):
    """Registration with verification email"""
    with patch("app.utils.send_verification_email", Mock()):
        response = client.post("/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "full_name": "Test User",
            "address": "123 Street",
            "phone": "1234567890",
            "role": "customer"
        })
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).filter_by(email="test@example.com").first()

def test_google_signup(client, db_session):
    """Google OAuth registration"""
    mock_user = {
        "email": "test@google.com",
        "full_name": "Google User",
        "google_id": "123",
        "email_verified": True
    }
    with patch("app.utils.auth_utils.verify_google_token", return_value=mock_user):
        response = client.post("/google-signup", params={"id_token": "valid"})
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).filter_by(email="test@google.com").first()

# 2. Profile Endpoints --------------------------------------------------------
@pytest.fixture
def auth_user(db_session):
    """Pre-authenticated test user"""
    user = User(
        user_id=1,
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        address="123 Street",
        phone="1234567890"
    )
    db_session.add(user)
    db_session.commit()
    return user

def test_get_profile(client, auth_user):
    """Profile retrieval"""
    with patch("app.utils.get_current_user", return_value=auth_user):
        response = client.get("/profile")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "test@example.com"

def test_update_profile(client, db_session, auth_user):
    """Full profile update"""
    with patch("app.utils.get_current_user", return_value=auth_user):
        response = client.patch("/profile", json={
            "full_name": "New Name",
            "phone": "9876543210"
        })
        assert response.status_code == status.HTTP_200_OK
        
        db_session.refresh(auth_user)
        assert auth_user.full_name == "New Name"
        assert auth_user.phone == "9876543210"

def test_partial_update(client, db_session, auth_user):
    """Single field update"""
    with patch("app.utils.get_current_user", return_value=auth_user):
        response = client.patch("/profile", json={"phone": "9876543210"})
        assert response.status_code == status.HTTP_200_OK
        
        db_session.refresh(auth_user)
        assert auth_user.phone == "9876543210"

def test_empty_update(client, auth_user):
    """Empty payload update"""
    with patch("app.utils.get_current_user", return_value=auth_user):
        response = client.patch("/profile", json={})
        assert response.status_code == status.HTTP_200_OK

# 3. Error Handling -----------------------------------------------------------
def test_unauthorized_access(client):
    """Unauthenticated profile access"""
    response = client.get("/profile")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_invalid_data(client, auth_user):
    """Invalid phone format"""
    with patch("app.utils.get_current_user", return_value=auth_user):
        response = client.patch("/profile", json={"phone": "invalid"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_nonexistent_user(client):
    """Update non-existent user"""
    with patch("app.utils.get_current_user", return_value=User(user_id=999)):
        response = client.patch("/profile", json={"full_name": "Ghost"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
