
from google.oauth2 import id_token
from google.auth.transport import requests
from passlib.context import CryptContext
from fastapi import HTTPException
import os
import json
import requests as http_requests

# Your Google Client ID
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class AuthUtils:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_google_token(self, token: str):
        print("Starting Google token verification...")
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            print("Decoded token claims:", id_info)

            if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                print(f"Invalid issuer: {id_info['iss']}")
                raise ValueError("Invalid issuer")

            if id_info["aud"] != GOOGLE_CLIENT_ID:
                print(f"Invalid audience: {id_info['aud']}")
                raise ValueError("Invalid audience")

            return {
                "google_id": id_info["sub"],
                "email": id_info["email"],
                "email_verified": id_info.get("email_verified", False),
                "full_name": id_info.get("name"),
            }
        except ValueError as e:
            print(f"Token verification failed: {str(e)}")
            return None

    def hash_password(self, password: str) -> str:
        """Hash a plain text password."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hashed password."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_google_auth_url(self):
        """Generate Google OAuth authorization URL."""
        client_id = GOOGLE_CLIENT_ID
        redirect_uri = "http://127.0.0.1:8000/auth/callback"
        scope = "openid email profile"
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}"
            f"&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
        )
        return auth_url

    def exchange_code_for_token(self, code: str):
        """Exchange authorization code for an access token."""
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "http://127.0.0.1:8000/auth/callback",
        }
        
        print("GOOGLE_CLIENT_SECRET:", os.getenv("GOOGLE_CLIENT_SECRET"))  
        response = http_requests.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch access token")
        return response.json()

# Initialize utility class
auth_utils = AuthUtils()







