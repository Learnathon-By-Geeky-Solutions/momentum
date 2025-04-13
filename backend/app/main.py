import uvicorn


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from app.models import User
from app.utils import auth_utils, create_access_token, verify_token
from app.database import get_db
from app.minio.routers import upload
import dotenv

from app.routers import (
    auth,
    brand,
    product,
    order,
    profile,
    paybill,
)  

from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import dotenv
import sentry_sdk
import os

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Range", "X-Content-Range"],
    max_age=600,
)


sentry_sdk.init(
    dsn="https://03bdab86608598f830e7193bd6e4db53@o4508298172497920.ingest.us.sentry.io/4508992259031040",
    send_default_pii=True,
    traces_sample_rate=1.0,
    instrumenter="otel",
)


dotenv.load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Include routers with prefixes and tags for organization
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="", tags=["Profile"])
app.include_router(brand.router, prefix="", tags=["Brands"])
app.include_router(product.router, prefix="", tags=["Products"])
app.include_router(upload.router, prefix="", tags=["Upload"])
app.include_router(order.router, prefix="", tags=["Orders"])
app.include_router(paybill.router, prefix="", tags=["Paybills"])
# app.include_router(agent.router, prefix="/agent", tags=["Agent"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
