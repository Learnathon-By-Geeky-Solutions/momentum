from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Annotated
from decimal import Decimal
import app.schemas as schemas
import app.models as models
from app.models import Order, OrderItem, Product, User, Brand
from app.database import get_db, SessionLocal
from app.utils import get_current_user


ORDER_NOT_FOUND = "Order not found"
router = APIRouter()


@router.post("/orders", response_model=schemas.OrderOut)
async def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    db_order = models.Order(
        user_id=current_user.user_id,
        status="Pending",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    total_amount = 0

    for item in order.order_items:

        product = (
            db.query(models.Product)
            .filter(models.Product.product_id == item.product_id)
            .first()
        )
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product with id {item.product_id} not found"
            )

        if (
            product.order_quantity is not None
            and item.quantity > product.order_quantity
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.product_name}",
            )

        item_cost = float(product.price) * item.quantity
        total_amount += item_cost

        db_order_item = models.OrderItem(
            order_id=db_order.order_id,
            product_id=item.product_id,
            size=item.size,
            quantity=item.quantity,
        )
        db.add(db_order_item)

    total_amount = Decimal(total_amount)
    db_bill = models.Bill(
        order_id=db_order.order_id,
        amount=total_amount,
        method="Pending",
        trx_id="1234",
        status="Pending",
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_order)
    return db_order


def place_order(user_id, product_id, size, quantity=1):

    session = SessionLocal()
    try:

        product = (
            session.query(Product)
            .filter(
                Product.product_id == product_id,
                Product.order_size == size,
            )
            .first()
        )

        if not product:
            return "Product not found or size unavailable."

        if product.order_quantity < quantity:
            return f"Sorry, only {product.order_quantity} items left in stock."

        new_order = Order(
            user_id=user_id,
            product_id=product_id,
            size=size,
            quantity=quantity,
            total_price=product.price * quantity,
        )
        session.add(new_order)

        product.order_quantity -= quantity
        session.commit()

        return f"Order placed successfully for {quantity} x {product.product_name} (Size: {size})!"

    except Exception as e:
        session.rollback()
        return f"Order placement error: {e}"

    finally:
        session.close()


@router.get("/orders/me")
async def get_my_orders(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.user_id)
        .all()
    )
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    base_url = "http://127.0.0.1:8000"

    orders_with_links = []
    for order in orders:
        order_data = {
            "order_id": order.order_id,
            "user_id": order.user_id,
            "status": order.status,
            "order_details_url": f"{base_url}/order/{order.order_id}",
            "product_details_url": f"{base_url}/order/{order.order_id}/products",
        }
        orders_with_links.append(order_data)
        print(order_data)

    return orders_with_links


@router.get("/orders/{order_id}/bill", response_model=schemas.BillOut)
async def get_bill_for_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=ORDER_NOT_FOUND)
    if order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view this order's bill",
        )

    bill = db.query(models.Bill).filter(models.Bill.order_id == order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")
    return bill


def _get_order_items_details(db: Session, order_id: int) -> List[dict]:
    order_items_query = (
        db.query(models.OrderItem, models.Product, models.Brand)
        .join(models.Product, models.OrderItem.product_id == models.Product.product_id)
        .join(models.Brand, models.Product.brand_id == models.Brand.brand_id)
        .filter(models.OrderItem.order_id == order_id)
        .all()
    )

    return [
        {
            "product_id": product.product_id,
            "brand_id": brand.brand_id,
            "product_name": product.product_name,
            "brand_name": brand.brand_name,
            "order_size": order_item.size,
            "order_quantity": order_item.quantity,
        }
        for order_item, product, brand in order_items_query
    ]


@router.get("/orders/{order_id}/details", response_model=schemas.OrderDetailOut)
async def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    order = (
        db.query(models.Order)
        .filter(
            models.Order.order_id == order_id,
            models.Order.user_id == current_user.user_id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail=ORDER_NOT_FOUND)

    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
    order_items = _get_order_items_details(db, order.order_id)

    return {
        "order_id": order.order_id,
        "status": order.status,
        "created_at": order.created_at,
        "bill_amount": bill.amount if bill else None,
        "order_items": order_items,
    }


@router.get("/orders/me/details", response_model=List[schemas.OrderDetailOut])
async def get_all_order_details(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.user_id)
        .all()
    )
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    orders_details = []
    for order in orders:
        bill = (
            db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
        )
        order_items = _get_order_items_details(db, order.order_id)

        order_data = {
            "order_id": order.order_id,
            "status": order.status,
            "bill_status": bill.status if bill else None,
            "created_at": order.created_at,
            "bill_amount": bill.amount if bill else None,
            "order_items": order_items,
        }
        orders_details.append(order_data)

    return orders_details


@router.delete("/orders/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    order = (
        db.query(models.Order)
        .filter(
            models.Order.order_id == order_id,
            models.Order.user_id == current_user.user_id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail=ORDER_NOT_FOUND)

    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")

    if bill.status.lower() != "pending":
        raise HTTPException(
            status_code=400,
            detail="Cannot delete order: bill is already confirmed or processed.",
        )

    db.delete(order)
    db.commit()

    return {"detail": "Order deleted successfully."}
