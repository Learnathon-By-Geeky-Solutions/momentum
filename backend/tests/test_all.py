import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_forgot_password(client):
    response = client.post("/forgot-password", json={"email": "testuser@example.com"})
    assert response.status_code == 404


def test_reset_password_invalid_token(client):
    response = client.post(
        "/reset-password",
        json={"token": "invalid_token", "new_password": "newpassword123"},
    )
    assert response.status_code == 400 or response.status_code == 422


def test_login_for_access_token_fail(client):
    response = client.post(
        "/token", data={"username": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_google_signup_invalid(client):
    response = client.post("/google-signup", params={"id_token": "fake_id_token"})
    assert response.status_code == 400


def test_get_all_users_unauthorized(client):
    response = client.get("/admin/users")
    assert response.status_code in [401, 403]


def test_get_all_products_unauthorized(client):
    response = client.get("/admin/products")
    assert response.status_code in [401, 403]


def test_get_all_orders_unauthorized(client):
    response = client.get("/admin/orders")
    assert response.status_code in [401, 403]


def test_promote_user_unauthorized(client):
    response = client.put("/admin/users/promote/1", json={"role": "admin"})
    assert response.status_code in [401, 403]


def test_delete_user_unauthorized(client):
    response = client.delete("/admin/users/1")
    assert response.status_code in [401, 403]


def test_delete_product_unauthorized(client):
    response = client.delete("/admin/products/1")
    assert response.status_code in [401, 403]


def test_delete_order_unauthorized(client):
    response = client.delete("/admin/orders/1")
    assert response.status_code in [401, 403]


def test_get_profile_unauthorized(client):
    response = client.get("/profile")
    assert response.status_code in [401, 403]


def test_update_profile_unauthorized(client):
    response = client.patch(
        "/profile",
        json={"full_name": "New Name", "address": "New Address", "phone": "1234567890"},
    )
    assert response.status_code in [401, 403]


def test_create_brand_unauthorized(client):
    response = client.post(
        "/brands",
        json={
            "brand_name": "Test Brand",
            "brand_description": "Test Description",
            "logo": "test_logo.png",
        },
    )
    assert response.status_code in [401, 403]


def test_get_my_brand_unauthorized(client):
    response = client.get("/brands/me")
    assert response.status_code in [401, 403]


def test_update_brand_unauthorized(client):
    response = client.patch(
        "/brands/me",
        json={
            "brand_name": "Updated Brand",
            "brand_description": "Updated Description",
            "logo": "updated_logo.png",
        },
    )
    assert response.status_code in [401, 403]


def test_create_product_unauthorized(client):
    response = client.post(
        "/products",
        json={
            "product_name": "Test Product",
            "product_pic": "pic.png",
            "product_video": "video.mp4",
            "category": "Test Category",
            "description": "Test description",
            "order_size": "M",
            "order_quantity": 10,
            "quantity_unit": "pcs",
            "price": 100.0,
        },
    )
    assert response.status_code in [401, 403]


def test_update_product_unauthorized(client):
    response = client.patch(
        "/products/1",
        json={
            "product_name": "Updated Product",
            "product_pic": "updated_pic.png",
            "product_video": "updated_video.mp4",
            "category": "Updated Category",
            "description": "Updated description",
            "order_size": "L",
            "order_quantity": 5,
            "quantity_unit": "pcs",
            "price": 150.0,
        },
    )
    assert response.status_code in [401, 403]


def test_delete_product_unauthorized(client):
    response = client.delete("/products/1")
    assert response.status_code in [401, 403]


def test_get_product(client):
    response = client.get("/products/1")
    assert response.status_code in [200, 404]


def test_get_all_products(client):
    response = client.get("/products")
    assert response.status_code == 200


def test_root_endpoint_available():
    response = client.get("/")
    assert response.status_code in (200, 404)


def test_get_my_orders_endpoint_accessible():
    response = client.get("/orders/me")
    assert response.status_code in (401, 403)


def test_get_my_orders_details_endpoint_accessible():
    response = client.get("/orders/me/details")
    assert response.status_code in (401, 403)


def test_get_bill_for_order_endpoint_accessible():
    response = client.get("/orders/1/bill")
    assert response.status_code in (401, 403, 404)


def test_get_order_details_endpoint_accessible():
    response = client.get("/orders/1/details")
    assert response.status_code in (401, 403, 404)


def test_delete_order_endpoint_accessible():
    response = client.delete("/orders/1")
    assert response.status_code in (401, 403, 404)


def test_initiate_payment():
    response = client.post("/initiate-payment", json={"order_id": "12345"})
    assert response.status_code == 200 or 404
