

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserUpdate
from database import get_db
from utils import get_current_user  # or from router.auth, depending on your structure
from typing import List, Optional
from fastapi import APIRouter


router = APIRouter()


# View Profile
@router.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "address": user.address,
        "phone": user.phone,
    }

# Update Profile
@router.put("/update-profile")
async def update_profile(user_update: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.full_name:
        db_user.full_name = user_update.full_name
    if user_update.address:
        db_user.address = user_update.address
    if user_update.phone:
        db_user.phone = user_update.phone

    db.commit()
    db.refresh(db_user)
    return {"message": "Profile updated successfully"}