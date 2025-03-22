from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Product, Order
from database import get_db
from utils import verify_token, oauth2_scheme
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)  # Should be a string, not a dictionary
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.email == user_email).first()
    if not user or user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user