from locust import HttpUser, task, between
import random
import string

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  

    def on_start(self):
        # Optional: any setup code per user session
        pass

    @task(2)  # Weight = 2 (this will be called twice as often as /register)
    def get_products(self):
        self.client.get("/products")

    @task(1)
    def register_user(self):
        random_username = ''.join(random.choices(string.ascii_lowercase, k=8))
        random_email = f"{random_username}@example.com"
        payload = {
            "username": random_username,
            "email": random_email,
            "password": "TestPassword123!",
            "full_name": "Test User",
            "address": "123 Testing Street",
            "phone": "1234567890",
            "role": "customer"  # whatever role your UserCreate expects
        }
        self.client.post("/register", json=payload)
