from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Product, Order
from database import get_db
from utils import verify_token, oauth2_scheme
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])

#Implement admin verification system for secure access control
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.email == user_email).first()
    if not user or user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return user

class PromoteUser(BaseModel):
    role: str

#Allow authorized admins to upgrade customer to admin
@router.put("/users/promote/{user_id}")
async def promote_user(
    user_id: int,
    role_data: PromoteUser,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    
    role = role_data.role.lower()
    
    if role_data.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Only 'admin' is allowed."
        )
    
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.role = role_data.role
    db.commit()
    db.refresh(user)
    return {"detail": f"User {user.username} is now an admin"}