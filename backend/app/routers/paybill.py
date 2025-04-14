from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.schemas as schemas, app.models as models
from app.database import get_db
from app.models import User, Order, OrderItem, Bill, Product
from app.schemas import PayBillRequest
from app.utils import get_current_user
from typing import List, Optional

from fastapi import APIRouter


router = APIRouter()


@router.post("/paybills")
def pay_bill(
    paybill_data: schemas.PayBillRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Confirm payment for an order:
      - Update the bill with the given method and trx_id, and mark its status as confirmed.
      - Decrease the stock (order_quantity) of each product based on the quantities in the order items.
    """
    order = (
        db.query(models.Order)
        .filter(
            models.Order.order_id == paybill_data.order_id,
            models.Order.user_id == current_user.user_id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")

    bill.method = paybill_data.method
    bill.trx_id = paybill_data.trx_id
    bill.status = "Confirmed"
    db.add(bill)
    db.commit()

    order_items = (
        db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == order.order_id)
        .all()
    )
    for item in order_items:
        product = (
            db.query(models.Product)
            .filter(models.Product.product_id == item.product_id)
            .first()
        )
        if product and product.order_quantity is not None:
            new_stock = product.order_quantity - item.quantity
            product.order_quantity = new_stock if new_stock >= 0 else 0
            db.add(product)

    db.commit()

    return {"message": "Bill confirmed and product stocks updated successfully."}
