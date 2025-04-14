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
from app.models import User, Order, OrderItem, Bill
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
    get_current_user,
    authenticate_user,
)
from app.database import get_db
from starlette.responses import JSONResponse
from app.routers import auth


app = FastAPI()


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app.include_router(auth.router)


# Error message constants
USER_NOT_FOUND = "User not found"
INVALID_CREDENTIALS = "Invalid credentials"
INVALID_TOKEN = "Invalid token or user not found"
INVALID_TOKEN_PAYLOAD = "Invalid token payload"
INVALID_RESET_TOKEN = "Invalid or expired token"
USER_ALREADY_EXISTS = "User with this email or username already exists."
PASSWORD_RESET_EMAIL_SENT = "If the email exists, a password reset link has been sent."
PASSWORD_RESET_SUCCESS = (
    "Password reset successful. You can now log in with your new password."
)
VERIFICATION_EMAIL_SENT = "Verification email sent. Please check your inbox."


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS,
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
        return {"message": PASSWORD_RESET_EMAIL_SENT}

    reset_token = create_reset_token(user.email)
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"

    # Use background tasks to send the email asynchronously
    background_tasks.add_task(send_reset_email, user.email, reset_link)

    return {"message": PASSWORD_RESET_EMAIL_SENT}


@router.post("/reset-password")
async def reset_password(
    request_data: ResetPasswordRequest, db: Session = Depends(get_db)
):
    email = verify_reset_token(request_data.token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_RESET_TOKEN
        )

    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )

    # Hash the new password and update
    hashed_password = auth_utils.hash_password(request_data.new_password)
    user.password = hashed_password
    db.commit()

    return {"message": PASSWORD_RESET_SUCCESS}


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and send a verification email"""

    existing_user = (
        db.query(User)
        .filter((User.email == user.email) | (User.username == user.username))
        .first()
    )

    if existing_user:
        raise HTTPException(status_code=400, detail=USER_ALREADY_EXISTS)

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
        content={"message": VERIFICATION_EMAIL_SENT},
    )


@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""

    user = db.query(User).filter(User.email == request.email).first()
    if not user or not auth_utils.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail=INVALID_CREDENTIALS)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
