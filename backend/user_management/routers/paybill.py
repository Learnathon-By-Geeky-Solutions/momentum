from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi import APIRouter

from user_management import schemas, models
from user_management.database import get_db
from user_management.utils import get_current_user


router = APIRouter()


@router.post("/paybill")
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
    # 1. Retrieve the order ensuring it belongs to the current user.
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

    # 2. Retrieve the corresponding bill
    bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found for this order")

    # 3. Update bill details: set the method, trx_id, and update status to "Confirmed"
    bill.method = paybill_data.method
    bill.trx_id = paybill_data.trx_id
    bill.status = (
        "Confirmed"  # or "True" if you prefer, but using a descriptive status is better
    )
    db.add(bill)
    db.commit()

    # 4. For each order item, decrease the product's available stock.
    order_items = (
        db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == order.order_id)
        .all()
    )
    for item in order_items:
        # Retrieve the product corresponding to the order item
        product = (
            db.query(models.Product)
            .filter(models.Product.product_id == item.product_id)
            .first()
        )
        if product and product.order_quantity is not None:
            # Decrease the product stock by the ordered quantity
            new_stock = product.order_quantity - item.quantity
            # Ensure stock doesn't go negative
            product.order_quantity = new_stock if new_stock >= 0 else 0
            db.add(product)

    db.commit()

    return {"message": "Bill confirmed and product stocks updated successfully."}
