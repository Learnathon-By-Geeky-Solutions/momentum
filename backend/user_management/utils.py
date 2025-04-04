



from fastapi import FastAPI, Depends, HTTPException,Header, APIRouter, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from user_management.database import SessionLocal, engine
from user_management.models import User
from user_management.schemas import UserCreate, Token, LoginRequest, UserUpdate, OrderOut, OrderCreate, PayBillRequest, ForgotPasswordRequest, ResetPasswordRequest
from datetime import timedelta
import os
import dotenv
from pydantic import BaseModel
import uvicorn
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing import Annotated
from decimal import Decimal

from fastapi import Security, HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests
from passlib.context import CryptContext
from fastapi import HTTPException
import os
import requests as http_requests
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from user_management.database import get_db


# Environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 100
RESET_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Google OAuth2 Client ID and Secret
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"



conf = ConnectionConfig(
    MAIL_USERNAME= os.getenv("mymail"),
    MAIL_PASSWORD=os.getenv("google_password"),
    MAIL_FROM= os.getenv("mymail"),
    MAIL_PORT=587,  # 587 for TLS, 465 for SSL
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Correct key name
    MAIL_SSL_TLS=False,  # Correct key name
    USE_CREDENTIALS=True
)


class AuthUtils:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_google_token(self, token: str):
        """Verify Google OAuth token."""
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                raise ValueError("Invalid issuer")
            if id_info["aud"] != GOOGLE_CLIENT_ID:
                raise ValueError("Invalid audience")

            return {
                "google_id": id_info["sub"],
                "email": id_info["email"],
                "email_verified": id_info.get("email_verified", False),
                "full_name": id_info.get("name"),
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Token verification failed: {str(e)}")

    def hash_password(self, password: str) -> str:
        """Hash a plain text password."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hashed password."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_google_auth_url(self):
        """Generate Google OAuth authorization URL."""
        scope = "openid email profile"
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"
        )
        return auth_url

    def exchange_code_for_token(self, code: str):
        """Exchange authorization code for an access token."""
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }
        response = http_requests.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch access token")
        return response.json()
    
def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError("No email found in token")
        return email
    except JWTError:
        return None

def create_email_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def send_verification_email(email: str, token: str):
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"Click the link to verify your email: {verification_link}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)





async def send_reset_email(email: str, link: str):
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=f"Click the link to reset your password: {link}",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    
    



    
def generate_verification_token(email: str):
    
    expire = datetime.utcnow() + timedelta(minutes=15)  # Token expires in 15 min
    data = {"sub": email, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    



def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return decoded data if valid
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user


# Initialize utility class
auth_utils = AuthUtils()


















