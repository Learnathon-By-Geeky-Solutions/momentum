from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Header,
    APIRouter,
    BackgroundTasks,
    status,
    Request,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated, List, Optional
from passlib.context import CryptContext
from app.models import User, Order, OrderItem, Bill  # adjust as needed
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
    verify_token,
    create_email_verification_token,
    send_verification_email,
    verify_reset_token,
    create_reset_token,
    send_reset_email,
)
from app.database import get_db
from starlette.responses import JSONResponse
from app.routers import auth


app = FastAPI()


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app.include_router(auth.router)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"

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

    # Hash the new password and update
    hashed_password = auth_utils.hash_password(request_data.new_password)
    user.password = hashed_password
    db.commit()

    return {
        "message": "Password reset successful. You can now log in with your new password."
    }


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and send a verification email"""

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

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name,
        address=user.address,
        phone=user.phone,
        role=user.role,  # Role is now validated
        is_verified=False,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_email_verification_token(user.email)
    await send_verification_email(user.email, token)

    return JSONResponse(
        status_code=200,
        content={"message": "Verification email sent. Please check your inbox."},
    )


@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not auth_utils.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Authenticate user from DB
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not auth_utils.verify_password(password, user.password):
        return False
    return user


# Get current user from token
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = verify_token(token)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user
