<<<<<<< HEAD


from fastapi import FastAPI, Depends, HTTPException, Header, APIRouter, BackgroundTasks, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated, List, Optional
from passlib.context import CryptContext
from models import User, Order, OrderItem, Bill  # adjust as needed
from schemas import UserCreate, Token, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from utils import auth_utils, create_access_token, verify_token, create_email_verification_token, send_verification_email, verify_reset_token, create_reset_token, send_reset_email
from database import get_db
from starlette.responses import JSONResponse
from routers import auth 



app = FastAPI()
=======
from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from user_management.models import User
from user_management.schemas import (
    UserCreate,
    Token,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from user_management.utils import (
    auth_utils,
    create_access_token,
    verify_token,
    create_email_verification_token,
    send_verification_email,
    verify_reset_token,
    create_reset_token,
    send_reset_email,
)
from user_management.database import get_db
>>>>>>> backend


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


<<<<<<< HEAD
app.include_router(auth.router)


@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request_data.email).first()
    
    # For security, return the same message even if the user is not found.
    if not user:
        return {"message": "If the email exists, a password reset link has been sent."}
    
    reset_token = create_reset_token(user.email)
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
    
    # Use background tasks to send the email asynchronously
    background_tasks.add_task(send_reset_email, user.email, reset_link)
    
    return {"message": "If the email exists, a password reset link has been sent."}

    

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = verify_reset_token(request_data.token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    
    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
=======
@router.post("/forgot-password")
async def forgot_password(
    request_data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == request_data.email).first()

    # For security, return the same message even if the user is not found.
    if not user:
        return {"message": "If the email exists, a password reset link has been sent."}

    reset_token = create_reset_token(user.email)
    reset_link = (
        f"http://localhost:3000/momentum/account/reset-password?token={reset_token}"
    )

    # Use background tasks to send the email asynchronously
    background_tasks.add_task(send_reset_email, user.email, reset_link)

    return {"message": "If the email exists, a password reset link has been sent."}


@router.post("/reset-password")
async def reset_password(
    request_data: ResetPasswordRequest, db: Session = Depends(get_db)
):
    email = verify_reset_token(request_data.token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )

    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

>>>>>>> backend
    # Hash the new password and update
    hashed_password = auth_utils.hash_password(request_data.new_password)
    user.password = hashed_password
    db.commit()
<<<<<<< HEAD
    
    return {"message": "Password reset successful. You can now log in with your new password."}

=======

    return {
        "message": "Password reset successful. You can now log in with your new password."
    }
>>>>>>> backend


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and send a verification email"""

<<<<<<< HEAD
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists.")
    

    hashed_password = auth_utils.hash_password(user.password)

    
=======
    existing_user = (
        db.query(User)
        .filter((User.email == user.email) | (User.username == user.username))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email or username already exists."
        )

    hashed_password = auth_utils.hash_password(user.password)

>>>>>>> backend
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        address=user.address,
        phone=user.phone,
<<<<<<< HEAD
        role=user.role,  # Role is now validated
        is_verified=False  
=======
        is_verified=False,
>>>>>>> backend
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
<<<<<<< HEAD

    token = create_email_verification_token(user.email)
    await send_verification_email(user.email, token)

    return JSONResponse(status_code=200, content={"message": "Verification email sent. Please check your inbox."})
=======
    token = create_email_verification_token(user.email)

    await send_verification_email(user.email, token)

    return JSONResponse(
        status_code=200,
        content={"message": "Verification email sent. Please check your inbox."},
    )
>>>>>>> backend


@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not auth_utils.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

<<<<<<< HEAD
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


=======
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "user": user}


@router.post("/verify-email")
async def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    token = request.token
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")

    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    db.commit()

    return {"message": "Email verified successfully"}

>>>>>>> backend

# Authenticate user from DB
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not auth_utils.verify_password(password, user.password):
        return False
    return user


<<<<<<< HEAD

# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
=======
# Get current user from token
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
>>>>>>> backend
    payload = verify_token(token)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user
<<<<<<< HEAD

=======
>>>>>>> backend
