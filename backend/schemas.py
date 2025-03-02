

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    username: Optional[str]
    email: str
    password: str
    full_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]

class UserOut(BaseModel):
    user_id: int
    username: Optional[str]
    email: str
    full_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    role: str  # New field in response

    class Config:
        from_attributes = True  # Pydantic v2 update
        



class LoginRequest(BaseModel):
    email: str
    password: str




class BrandCreate(BaseModel):
    #user_id: int  # Ensure the user exists before creating a brand
    brand_name: str
    brand_description: Optional[str]
    logo: Optional[str]

class BrandOut(BaseModel):
    brand_id: int
    user_id: int
    brand_name: str
    brand_description: Optional[str]
    logo: Optional[str]
    created_at: datetime  # Keep it as datetime

    class Config:
        from_attributes = True  # Pydantic v2 update

class ProductCreate(BaseModel):
    #brand_id: int  # Ensure the brand exists before creating a product
    product_name: str
    product_pic: List[str]  # Array of image storage links
    product_video: List[str]  # Array of video storage links
    category: str
    description: Optional[str]
    order_size: Optional[str]
    order_quantity: Optional[int]
    quantity_unit: Optional[str]
    price: float

class ProductOut(BaseModel):
    product_id: int
    #brand_id: int
    product_name: str
    product_pic: List[str]
    product_video: List[str]
    category: str
    description: Optional[str]
    order_size: Optional[str]
    order_quantity: Optional[int]
    quantity_unit: Optional[str]
    price: float
    rating: Optional[float]  # Given by buyers, not the product creator
    approved: bool  # Fulfilled by admin

    class Config:
        from_attributes = True  # Pydantic v2 update
        

class ProductUpdate(BaseModel):
    product_id: int
    brand_id: int
    product_name: str
    product_pic: List[str]
    product_video: List[str]
    category: str
    description: Optional[str]
    order_size: Optional[str]
    order_quantity: Optional[int]
    quantity_unit: Optional[str]
    price: float
    rating: Optional[float]  # Given by buyers, not the product creator
    approved: bool  # Fulfilled by admin
        
        
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
