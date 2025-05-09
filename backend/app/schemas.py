from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import re


class RegistrationResponse(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class TokenData(BaseModel):
    email: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="Password must be between 8-50 characters.",
    )

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", value
        ):
            raise ValueError(
                "Password must contain at least one letter, one number, and one special character."
            )
        return value


class UserCreate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: EmailStr  # Ensures valid email format
    password: str = Field(..., min_length=8, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(
        None,
        pattern=r"^(?:\+88|01)?(?:\d{9,10})$",
        description="Must be a valid BD phone number.",
    )
    role: str = Field(..., description="User role must be specified.")

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


class PromoteUser(BaseModel):
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)


class BrandCreate(BaseModel):
    brand_name: str = Field(..., min_length=3, max_length=100)
    brand_description: Optional[str] = Field(None, max_length=255)
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
    product_name: str = Field(..., min_length=3, max_length=100)
    product_pic: List[str]
    product_video: List[str]
    category: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=5500)
    order_size: Optional[str]
    order_quantity: Optional[int] = Field(None, ge=1)
    quantity_unit: Optional[str]
    price: float = Field(..., gt=0)


class ProductOut(BaseModel):
    product_id: int
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
    product_name: str
    category: str
    description: str
    price: float
    approved: bool


class ProductUpdate(ProductCreate):
    product_id: int


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, pattern=r"^(?:\+88|01)?(?:\d{9,10})$")


class OrderItemCreate(BaseModel):
    product_id: int
    size: Optional[str]
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate]
    address: Optional[str] = Field(None, max_length=255)
    phone: str


class OrderOut(BaseModel):
    order_id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    status: str


class BillCreate(BaseModel):
    amount: float = Field(..., gt=0)
    method: str = Field(..., min_length=3)
    trx_id: str = Field(..., min_length=5, max_length=50)
    status: str


class BillOut(BaseModel):
    bill_id: int
    order_id: int
    amount: int
    method: str
    trx_id: Optional[str]
    status: str

    class Config:
        orm_mode = True


class PayBillRequest(BaseModel):
    order_id: int
    method: str
    trx_id: str = Field(..., min_length=5, max_length=50)


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


class ChatRequest(BaseModel):
    messages: List[str]

    messages: List[str]


class ChatResponse(BaseModel):
    response: str
