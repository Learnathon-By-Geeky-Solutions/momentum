from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User, Product, Order
from app.database import get_db
from app.utils import get_current_admin
from app.schemas import UserUpdate, ProductUpdate, OrderUpdate, PromoteUser

router = APIRouter()


def get_object_or_404(model, object_id: int, db: Session, field="id", name="Item"):
    obj = db.query(model).filter(getattr(model, field) == object_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found"
        )
    return obj


def update_object_fields(db_obj, update_data):
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)


@router.put("/users/promote/{user_id}")
async def promote_user(
    user_id: int,
    role_data: PromoteUser,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    if role_data.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Only 'admin' is allowed.",
        )

    user = get_object_or_404(User, user_id, db, field="user_id", name="User")
    user.role = "admin"
    db.commit()
    db.refresh(user)
    return {"detail": f"User {user.username} is now an admin"}


@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return db.query(User).all()


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = get_object_or_404(User, user_id, db, field="user_id", name="User")
    update_object_fields(user, user_data)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = get_object_or_404(User, user_id, db, field="user_id", name="User")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


@router.get("/products")
async def get_all_products(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return db.query(Product).all()


@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    product = get_object_or_404(
        Product, product_id, db, field="product_id", name="Product"
    )
    update_object_fields(product, product_data)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    product = get_object_or_404(
        Product, product_id, db, field="product_id", name="Product"
    )
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}


@router.get("/orders")
async def get_all_orders(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return db.query(Order).all()


@router.put("/orders/{order_id}")
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    order = get_object_or_404(Order, order_id, db, field="order_id", name="Order")
    update_object_fields(order, order_data)
    db.commit()
    db.refresh(order)
    return order


@router.delete("/orders/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    order = get_object_or_404(Order, order_id, db, field="order_id", name="Order")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}
