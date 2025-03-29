<<<<<<< HEAD

from fastapi import FastAPI, Depends, HTTPException, Header, APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
from datetime import timedelta
import dotenv
from typing import Annotated
from models import User
from utils import auth_utils, create_access_token, verify_token

from routers import auth, brand, product, order, profile, paybill  # Import routers
import uvicorn
=======
import uvicorn


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from user_management.models import User
from user_management.utils import auth_utils, create_access_token, verify_token
from user_management.database import get_db

from user_management.routers import (
    auth,
    brand,
    product,
    order,
    profile,
    paybill,
)  # Import routers
from user_management.ai.routers import agent

import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware


sentry_sdk.init(
    dsn="https://03bdab86608598f830e7193bd6e4db53@o4508298172497920.ingest.us.sentry.io/4508992259031040",
    send_default_pii=True,
    traces_sample_rate=1.0,
    instrumenter="otel",
)
>>>>>>> backend


dotenv.load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

<<<<<<< HEAD

app = FastAPI()

# Include routers with prefixes and tags for organization
app.include_router(auth.router, prefix="", tags=["Auth"])
app.include_router(profile.router, prefix="", tags=["Profile"])
app.include_router(brand.router, prefix="", tags=["Brands"])
app.include_router(product.router, prefix="", tags=["Products"])
app.include_router(order.router, prefix="", tags=["Orders"])
app.include_router(paybill.router, prefix="", tags=["Paybills"])
#app.include_router(agent.router, prefix="/agent", tags=["Agent"])




=======
app = FastAPI()

# Include routers with prefixes and tags for organization
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/profiles", tags=["Profile"])
app.include_router(brand.router, prefix="/brands", tags=["Brands"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(paybill.router, prefix="/paybills", tags=["Paybills"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sentry-debug")
def trigger_error():
    division_by_zero = 1 / 0

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
@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
=======

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
>>>>>>> backend
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


<<<<<<< HEAD


=======
>>>>>>> backend
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
