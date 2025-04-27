from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.models import User
from app.schemas import (
    UserCreate,
    Token,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.utils import (
    auth_utils,
    create_access_token,
    create_email_verification_token,
    send_verification_email,
    verify_reset_token,
    create_reset_token,
    send_reset_email,
    authenticate_user,
)
from app.database import get_db

router = APIRouter()

INVALID_CREDENTIALS = "Invalid credentials"
USER_EXISTS = "User already exists."
USER_NOT_FOUND = "User not found"
PASSWORD_RESET_SUCCESS = "Password reset successful."
PASSWORD_RESET_SENT = "If the email exists, a password reset link has been sent."


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def raise_invalid_credentials():
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS)


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise_invalid_credentials()
    token = create_access_token({"sub": user.email}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
    if user.role == "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Admin cannot reset password")
    token = create_reset_token(user.email)
    link = f"http://localhost:8000/reset-password?token={token}"
    background_tasks.add_task(send_reset_email, user.email, link)
    return {"message": PASSWORD_RESET_SENT}


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = verify_reset_token(data.token)
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
    user.password = auth_utils.hash_password(data.new_password)
    db.commit()
    return {"message": PASSWORD_RESET_SUCCESS}


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter((User.email == user.email) | (User.username == user.username))
        .first()
    )
    if existing_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=USER_EXISTS)
    new_user = User(
        username=user.username,
        email=user.email,
        password=auth_utils.hash_password(user.password),
        full_name=user.full_name,
        address=user.address,
        phone=user.phone,
        role=user.role if user.role else "customer",
        is_verified=False,
    )
    db.add(new_user)
    db.commit()
    token = create_email_verification_token(user.email)
    await send_verification_email(user.email, token)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user or not auth_utils.verify_password(request.password, user.password):
        raise_invalid_credentials()
    token = create_access_token({"sub": user.email}, timedelta(minutes=30))
    data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "phone": user.phone,
        "role": user.role,
        "is_verified": user.is_verified,
        
    }
    return {"access_token": token, "token_type": "bearer" , "user": data}


@router.post("/google-signup")
def google_signup(id_token: str, db: Session = Depends(get_db)):
    try:
        user_info = auth_utils.verify_google_token(id_token)

        existing_user = db.query(User).filter(User.email == user_info["email"]).first()
        if existing_user:
            access_token = create_access_token({"sub": user_info["email"]})
            return {"access_token": access_token, "token_type": "bearer"}

        new_user = User(
            email=user_info["email"],
            full_name=user_info["full_name"],
            google_id=user_info["google_id"],
            is_verified=user_info["email_verified"],
            role="user",
            password=None,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token = create_access_token({"sub": new_user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
