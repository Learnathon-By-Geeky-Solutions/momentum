from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserUpdate
from app.database import get_db
from app.utils import (
    get_current_user,
)
from typing import List, Optional
from fastapi import APIRouter


router = APIRouter()


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


@router.patch("/profile")
async def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return {"message": "Profile updated successfully"}


@router.put("/become-artisan")
async def become_artisan(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user), 
):
    if user.role == "artisan":
        raise HTTPException(status_code=400, detail="You are already an artisan")
    user.role = "artisan"
    db.commit()
    db.refresh(user)
    return {"message": "You are now an artisan"}
