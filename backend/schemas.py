# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

# Response schema (does not include the password)
class UserOut(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True
