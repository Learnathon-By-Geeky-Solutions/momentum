
import pytest
from app.models import User, Product, Order


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



import pytest
from app.models import User, Product, Order



def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_user(client, db_session):
    user = User(username="testupdate", email="testupdate@example.com", password="hashed", role="customer")
    db_session.add(user)
    db_session.commit()

    update_data = {"full_name": "Updated Name"}
    response = client.put(f"/users/{user.user_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"

def test_delete_user(client, db_session):
    user = User(username="testdelete", email="testdelete@example.com", password="hashed", role="customer")
    db_session.add(user)
    db_session.commit()

    response = client.delete(f"/users/{user.user_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"

def test_promote_user(client, db_session):
    user = User(username="promoteme", email="promoteme@example.com", password="hashed", role="customer")
    db_session.add(user)
    db_session.commit()

    response = client.put(f"/users/promote/{user.user_id}", json={"role": "admin"})
    assert response.status_code == 200
    assert "now an admin" in response.json()["detail"]

def test_promote_user_invalid_role(client, db_session):
    user = User(username="badpromote", email="badpromote@example.com", password="hashed", role="customer")
    db_session.add(user)
    db_session.commit()

    response = client.put(f"/users/promote/{user.user_id}", json={"role": "invalid"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid role. Only 'admin' is allowed."

def test_update_user_not_found(client):
    response = client.put("/users/9999", json={"full_name": "Test"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"



def test_get_all_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product(client, db_session):
    product = Product(product_name="Test Product", category="Test", price=10.0)
    db_session.add(product)
    db_session.commit()

    update_data = {"price": 20}
    response = client.put(f"/products/{product.product_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["price"] == 20

def test_delete_product(client, db_session):
    product = Product(product_name="Delete Product", category="Test", price=10.0)
    db_session.add(product)
    db_session.commit()

    response = client.delete(f"/products/{product.product_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Product deleted successfully"

def test_update_product_not_found(client):
    response = client.put("/products/9999", json={"price": 50.0})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_delete_product_not_found(client):
    response = client.delete("/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_all_orders(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_order(client, db_session):
    order = Order(order_size="M", order_quantity=1, quantity_unit="pcs", price=100)
    db_session.add(order)
    db_session.commit()

    update_data = {"price": 150}
    response = client.put(f"/orders/{order.order_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["price"] == 150

def test_delete_order(client, db_session):
    order = Order(order_size="L", order_quantity=2, quantity_unit="pcs", price=200)
    db_session.add(order)
    db_session.commit()

    response = client.delete(f"/orders/{order.order_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Order deleted successfully"

def test_update_order_not_found(client):
    response = client.put("/orders/9999", json={"price": 123})
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

def test_delete_order_not_found(client):
    response = client.delete("/orders/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"
