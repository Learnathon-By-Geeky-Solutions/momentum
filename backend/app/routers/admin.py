from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Product, Order
from database import get_db
from utils import get_current_admin
from schemas import UserUpdate, ProductUpdate, OrderUpdate
from schemas import PromoteUser

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.put("/users/promote/{user_id}")
async def promote_user(
    user_id: int,
    role_data: PromoteUser,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    role = role_data.role.lower()

    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Only 'admin' is allowed.",
        )

    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.role = role
    db.commit()
    db.refresh(user)
    return {"detail": f"User {user.username} is now an admin"}

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)
):
    users = db.query(User).all()
    return users


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

@router.get("/products")
async def get_all_products(
    db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)
):
    products = db.query(Product).all()
    return products


@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

@router.get("/orders")
async def get_all_orders(
    db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)
):
    orders = db.query(Order).all()
    return orders


@router.put("/orders/{order_id}")
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    for key, value in order_data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


@router.delete("/orders/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}
