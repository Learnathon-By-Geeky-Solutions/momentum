from app.models import User


def test_register(client, db_session):
    user_data = {
        "username": "testuser03",
        "email": "testuser03@example.com",
        "password": "testpassword",
        "full_name": "Test User",
        "address": "123 Test Street",
        "phone": "1234567890",
        "role": "customer",
    }

    response = client.post("/register", json=user_data)

    print("Response JSON:", response.json())
    print("Response Status Code:", response.status_code)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Verification email sent. Please check your inbox."
    }

    user = db_session.query(User).filter(User.email == user_data["email"]).first()
    assert user is not None
    assert user.email == user_data["email"]
