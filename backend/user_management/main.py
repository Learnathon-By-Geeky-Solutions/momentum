
from fastapi import FastAPI, Depends, HTTPException, Header, APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import timedelta
import os
import dotenv
from typing import Annotated, List, Optional
from decimal import Decimal
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from models import User, Order, OrderItem, Bill  # adjust as needed
from utils import auth_utils, create_access_token, verify_token, create_email_verification_token, send_verification_email, verify_reset_token, create_reset_token, send_reset_email
from database import get_db

from routers import auth, brand, product, order, profile, paybill  # Import routers
from ai.routers import agent



from fastapi import FastAPI
import uvicorn


dotenv.load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

# Include routers with prefixes and tags for organization
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/profiles", tags=["Profile"])
app.include_router(brand.router, prefix="/brands", tags=["Brands"])
app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(paybill.router, prefix="/paybills", tags=["Paybills"])
app.include_router(agent.router, prefix="/agent", tags=["Agent"])





# Authenticate user from DB
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not auth_utils.verify_password(password, user.password):
        return False
    return user



# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
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




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
