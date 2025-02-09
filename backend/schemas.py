from pydantic import BaseModel  
from typing import Optional  
  
# Schema for creating a new user  
class UserCreate(BaseModel):  
    username: str  
    email: str  
    password: str  
    full_name: Optional[str]  
    address: Optional[str]  
    phone: Optional[str]  
  
# Schema for logging in a user  
class UserLogin(BaseModel):  
    email: str  
    password: str  
  
# Schema for returning user data  
class UserOut(BaseModel):  
    user_id: int  # Changed from `id` to match the `user_id` in your model  
    username: Optional[str]  
    email: str  
    full_name: Optional[str]  
    address: Optional[str]  
    phone: Optional[str]  
    google_id: Optional[str]  # Include google_id for Google Sign-In users  
  
    class Config:  
        orm_mode = True  