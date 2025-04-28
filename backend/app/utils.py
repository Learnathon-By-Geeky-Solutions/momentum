import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Security, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as http_requests
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.database import get_db

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60 * 60
RESET_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60 * 60
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"

MAIL_USERNAME = os.getenv("mymail")
MAIL_PASSWORD = os.getenv("google_password")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_USERNAME,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

INVALID_TOKEN = "Invalid token"
INVALID_OR_EXPIRED_TOKEN = "Invalid or expired token"
INVALID_TOKEN_PAYLOAD = "Invalid token payload"
USER_NOT_FOUND = "User not found"
NOT_ENOUGH_PERMISSIONS = "Not enough permissions"


class AuthUtils:
    def verify_google_token(self, token: str):
        try:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_CLIENT_ID
            )
            if (
                id_info["iss"]
                not in ["accounts.google.com", "https://accounts.google.com"]
                or id_info["aud"] != GOOGLE_CLIENT_ID
            ):
                raise ValueError(INVALID_TOKEN)
            return {
                "google_id": id_info["sub"],
                "email": id_info["email"],
                "email_verified": id_info.get("email_verified", False),
                "full_name": id_info.get("name"),
            }
        except ValueError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=INVALID_TOKEN)

    def get_google_auth_url(self):
        scope = "openid email profile"
        return (
            f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"
        )

    def exchange_code_for_token(self, code: str):
        data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }
        response = http_requests.post("https://oauth2.googleapis.com/token", data=data)
        if response.status_code != 200:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=INVALID_TOKEN)
        return response.json()

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


auth_utils = AuthUtils()


def create_token(data: dict, expires_minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_reset_token(email: str):
    return create_token({"sub": email}, RESET_TOKEN_EXPIRE_MINUTES)


def verify_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=INVALID_TOKEN)
        return email
    except JWTError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=INVALID_OR_EXPIRED_TOKEN
        )


def create_email_verification_token(email: str):
    return create_token({"sub": email}, 60)


async def send_email(subject: str, email: str, body: str):
    message = MessageSchema(
        subject=subject, recipients=[email], body=body, subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_verification_email(email: str, token: str):
    baseUrl = os.getenv("BASE_URL")
    link = f"{baseUrl}/account/verify-email?token={token}"
    await send_email(
        "Verify Your Email", email, f"Click the link to verify your email: {link}"
    )


async def send_reset_email(email: str, link: str):
    await send_email(
        "Reset Your Password", email, f"Click the link to reset your password: {link}"
    )


def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Security(oauth2_scheme)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_TOKEN,
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and auth_utils.verify_password(password, user.password):
        return user
    return False


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = verify_token(token)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=INVALID_TOKEN_PAYLOAD)
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=USER_NOT_FOUND)
    return user


def get_current_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=NOT_ENOUGH_PERMISSIONS)
    return user
