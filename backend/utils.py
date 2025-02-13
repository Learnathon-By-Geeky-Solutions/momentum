

from google.oauth2 import id_token
from google.auth.transport import requests
from passlib.context import CryptContext
from fastapi import HTTPException
import os
import requests as http_requests
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

# Environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_key")  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Google OAuth2 Client ID and Secret
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"


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


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """Verify JWT token and extract email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


# Initialize utility class
auth_utils = AuthUtils()






















# from google.oauth2 import id_token
# from google.auth.transport import requests
# from passlib.context import CryptContext
# from fastapi import HTTPException
# import os
# import json
# import requests as http_requests
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from fastapi.security import OAuth2PasswordBearer

# # Environment variables
# SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mysecretkey")  # Change this in production
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Google OAuth2 Client ID
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


# class AuthUtils:
#     def __init__(self):
#         self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#     def verify_google_token(self, token: str):
#         """Verify Google OAuth token."""
#         print("Starting Google token verification...")
#         try:
#             id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
#             print("Decoded token claims:", id_info)

#             if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
#                 print(f"Invalid issuer: {id_info['iss']}")
#                 raise ValueError("Invalid issuer")

#             if id_info["aud"] != GOOGLE_CLIENT_ID:
#                 print(f"Invalid audience: {id_info['aud']}")
#                 raise ValueError("Invalid audience")

#             return {
#                 "google_id": id_info["sub"],
#                 "email": id_info["email"],
#                 "email_verified": id_info.get("email_verified", False),
#                 "full_name": id_info.get("name"),
#             }
#         except ValueError as e:
#             print(f"Token verification failed: {str(e)}")
#             return None
        
        
        
#     def hash_password(password: str) -> str:
#         """Hash a password securely"""
#         return pwd_context.hash(password)


#     # def hash_password(self, password: str) -> str:
#     #     """Hash a plain text password."""
#     #     return self.pwd_context.hash(password)

#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         """Verify a plain text password against a hashed password."""
#         return self.pwd_context.verify(plain_password, hashed_password)

#     def get_google_auth_url(self):
#         """Generate Google OAuth authorization URL."""
#         client_id = GOOGLE_CLIENT_ID
#         redirect_uri = "http://127.0.0.1:8000/auth/callback"
#         scope = "openid email profile"
#         auth_url = (
#             f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}"
#             f"&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
#         )
#         return auth_url

#     def exchange_code_for_token(self, code: str):
#         """Exchange authorization code for an access token."""
#         token_url = "https://oauth2.googleapis.com/token"
#         data = {
#             "client_id": GOOGLE_CLIENT_ID,
#             "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
#             "code": code,
#             "grant_type": "authorization_code",
#             "redirect_uri": "http://127.0.0.1:8000/auth/callback",
#         }
        
#         print("GOOGLE_CLIENT_SECRET:", os.getenv("GOOGLE_CLIENT_SECRET"))  
#         response = http_requests.post(token_url, data=data)
#         if response.status_code != 200:
#             raise HTTPException(status_code=400, detail="Failed to fetch access token")
#         return response.json()


# ### **Move JWT Functions Outside the Class** ###
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     """Create a JWT access token."""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def verify_token(token: str):
#     """Verify JWT token and extract email."""
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return email
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")


# # Initialize utility class
# auth_utils = AuthUtils()



# from google.oauth2 import id_token
# from google.auth.transport import requests
# from passlib.context import CryptContext
# from fastapi import HTTPException, Depends
# import os
# import json

# import requests as http_requests
# from datetime import datetime, timedelta
# from jose import jwt, JWTError  # Ensure correct import
# from fastapi.security import OAuth2PasswordBearer

# # Load secret key properly
# SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mysecretkey")  # Change in production
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Google OAuth config
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"


# class AuthUtils:
#     def __init__(self):
#         self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#     def verify_google_token(self, token: str):
#         """Verify Google OAuth token"""
#         try:
#             id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
#             if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
#                 raise ValueError("Invalid issuer")
#             if id_info["aud"] != GOOGLE_CLIENT_ID:
#                 raise ValueError("Invalid audience")

#             return {
#                 "google_id": id_info["sub"],
#                 "email": id_info["email"],
#                 "email_verified": id_info.get("email_verified", False),
#                 "full_name": id_info.get("name"),
#             }
#         except ValueError:
#             return None

#     def hash_password(self, password: str) -> str:
#         return self.pwd_context.hash(password)

#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         return self.pwd_context.verify(plain_password, hashed_password)

#     def get_google_auth_url(self):
#         """Generate Google OAuth URL"""
#         scope = "openid email profile"
#         auth_url = (
#             f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}"
#             f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"
#         )
#         return auth_url

#     def exchange_code_for_token(self, code: str):
#         """Exchange Google Auth Code for Token"""
#         token_url = "https://oauth2.googleapis.com/token"
#         data = {
#             "client_id": GOOGLE_CLIENT_ID,
#             "client_secret": GOOGLE_CLIENT_SECRET,
#             "code": code,
#             "grant_type": "authorization_code",
#             "redirect_uri": REDIRECT_URI,
#         }
#         response = http_requests.post(token_url, data=data)
#         if response.status_code != 200:
#             raise HTTPException(status_code=400, detail="Failed to fetch access token")
#         return response.json()

#     def create_access_token(self, data: dict, expires_delta: timedelta = None):
#         """Create JWT Access Token"""
#         to_encode = data.copy()
#         expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#         to_encode.update({"exp": expire})
#         return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     def verify_token(self, token: str):
#         """Verify JWT Token"""
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             email = payload.get("sub")
#             if email is None:
#                 raise HTTPException(status_code=401, detail="Invalid token")
#             return email
#         except JWTError:
#             raise HTTPException(status_code=401, detail="Could not validate credentials")


# # Initialize the utility class
# auth_utils = AuthUtils()







# from google.oauth2 import id_token
# from google.auth.transport import requests
# from passlib.context import CryptContext
# from fastapi import HTTPException
# import os
# import json
# import requests as http_requests

# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from fastapi import HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer





# SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mysecretkey")  # Change this in production
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Your Google Client ID
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


# class AuthUtils:
#     def __init__(self):
#         self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#     def verify_google_token(self, token: str):
#         print("Starting Google token verification...")
#         try:
#             id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
#             print("Decoded token claims:", id_info)

#             if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
#                 print(f"Invalid issuer: {id_info['iss']}")
#                 raise ValueError("Invalid issuer")

#             if id_info["aud"] != GOOGLE_CLIENT_ID:
#                 print(f"Invalid audience: {id_info['aud']}")
#                 raise ValueError("Invalid audience")

#             return {
#                 "google_id": id_info["sub"],
#                 "email": id_info["email"],
#                 "email_verified": id_info.get("email_verified", False),
#                 "full_name": id_info.get("name"),
#             }
#         except ValueError as e:
#             print(f"Token verification failed: {str(e)}")
#             return None

#     def hash_password(self, password: str) -> str:
#         """Hash a plain text password."""
#         return self.pwd_context.hash(password)

#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         """Verify a plain text password against a hashed password."""
#         return self.pwd_context.verify(plain_password, hashed_password)

#     def get_google_auth_url(self):
#         """Generate Google OAuth authorization URL."""
#         client_id = GOOGLE_CLIENT_ID
#         redirect_uri = "http://127.0.0.1:8000/auth/callback"
#         scope = "openid email profile"
#         auth_url = (
#             f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}"
#             f"&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
#         )
#         return auth_url

#     def exchange_code_for_token(self, code: str):
#         """Exchange authorization code for an access token."""
#         token_url = "https://oauth2.googleapis.com/token"
#         data = {
#             "client_id": GOOGLE_CLIENT_ID,
#             "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
#             "code": code,
#             "grant_type": "authorization_code",
#             "redirect_uri": "http://127.0.0.1:8000/auth/callback",
#         }
        
#         print("GOOGLE_CLIENT_SECRET:", os.getenv("GOOGLE_CLIENT_SECRET"))  
#         response = http_requests.post(token_url, data=data)
#         if response.status_code != 200:
#             raise HTTPException(status_code=400, detail="Failed to fetch access token")
#         return response.json()
    
    
    
    
         
#     def create_access_token(data: dict, expires_delta: timedelta = None):
#         to_encode = data.copy()
#         expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#         to_encode.update({"exp": expire})
#         return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     def verify_token(token: str):
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             email = payload.get("sub")
#             if email is None:
#                 raise HTTPException(status_code=401, detail="Invalid token")
#             return email
#         except JWTError:
#             raise HTTPException(status_code=401, detail="Could not validate credentials")
    

# # Initialize utility class
# auth_utils = AuthUtils()





# {
#   "username": "ll",
#   "email": "ll@gmail.com",
#   "password": "1234",
#   "full_name": "llll",
#   "address": "ctg",
#   "phone": "012345"
# }






