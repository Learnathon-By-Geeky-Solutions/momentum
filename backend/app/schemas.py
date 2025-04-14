from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    email: Optional[str] = None




class ForgotPasswordRequest(BaseModel):
    email: EmailStr



class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str



class UserCreate(BaseModel):
    username: Optional[str]
    email: str
    password: str
    full_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    role: Optional[str] = "customer"


    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        value = value.lower()
        if value not in ["customer", "artisan"]:
            raise ValueError("Invalid role. Allowed values: 'customer' or 'artisan'.")
        return value


class UserOut(BaseModel):
    user_id: int
    username: Optional[str]
    email: str
    full_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class BrandCreate(BaseModel):
    brand_name: str
    brand_description: Optional[str]
    logo: Optional[str]



class BrandOut(BaseModel):
    brand_id: int
    user_id: int
    brand_name: str
    brand_description: Optional[str]
    logo: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    product_name: str
    product_pic: List[str]
    product_video: List[str]
    category: str
    description: Optional[str]
    order_size: Optional[str]
    order_quantity: Optional[int]
    quantity_unit: Optional[str]
    price: float



class ProductOut(BaseModel):
    product_id: int
    # brand_id: int
    # brand_id: int
    product_name: str
    product_pic: List[str]
    product_video: List[str]
    category: str
    description: Optional[str]
    order_size: Optional[str]
    order_quantity: Optional[int]
    quantity_unit: Optional[str]
    price: float
    rating: Optional[float]
    approved: bool

    class Config:
        from_attributes = True


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
    rating: Optional[float]
    approved: bool


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class OrderItemCreate(BaseModel):
    product_id: int
    size: Optional[str]
    quantity: int


class BillCreate(BaseModel):
    amount: float
    method: str
    trx_id: str
    status: str


class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate]


class OrderOut(BaseModel):
    order_id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True
class OrderItemCreate(BaseModel):
    product_id: int
    size: Optional[str]
    quantity: int


class BillCreate(BaseModel):
    amount: float
    method: str
    trx_id: str
    status: str


class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate]


class OrderOut(BaseModel):
    order_id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True


class BillOut(BaseModel):
    bill_id: int
    order_id: int
    amount: int
    method: str
    trx_id: Optional[str]
    status: str

    class Config:
        orm_mode = True


class OrderItemDetail(BaseModel):
    product_id: int
    brand_id: int
    product_name: str
    brand_name: str
    order_size: str
    order_quantity: int



class OrderDetailOut(BaseModel):
    order_id: int
    status: str
    bill_status: Optional[str] = None
    created_at: datetime
    bill_amount: Optional[Decimal]
    order_items: List[OrderItemDetail]

    class Config:
        orm_mode = True



class PayBillRequest(BaseModel):
    order_id: int
    method: str
    trx_id: str


# class Message(BaseModel):
#     role: str
#     content: str



class ChatRequest(BaseModel):
    messages: List[str]


    messages: List[str]


class ChatResponse(BaseModel):
    response: str

