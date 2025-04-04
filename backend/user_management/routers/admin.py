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

#Add user management functionality for admin
class UserUpdate(BaseModel):
    username: str
    email: str
    full_name: str
    address: str
    phone: str
    
@router.get("/users")
async def get_all_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    users = db.query(User).all()
    return users

@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

#Add product management functionality for admin
class ProductUpdate(BaseModel):
    product_name: str
    category: str
    description: str
    price: float
    approved: bool

@router.get("/products")
async def get_all_products(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    products = db.query(Product).all()
    return products

@router.put("/products/{product_id}")
async def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

#Add order management functionality for admin
class OrderUpdate(BaseModel):
    status: str

@router.get("/orders")
async def get_all_orders(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    orders = db.query(Order).all()
    return orders

@router.put("/orders/{order_id}")
async def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for key, value in order_data.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order

@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}