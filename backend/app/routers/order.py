from fastapi import APIRouter, Depends, HTTPException, status  
from sqlalchemy.orm import Session  
from typing import List  
from decimal import Decimal  
import app.schemas as schemas  
import app.models as models  
from app.database import get_db, SessionLocal  
from app.utils import get_current_user  
  
router = APIRouter()  
  
ORDER_NOT_FOUND = "Order not found"  
PRODUCT_NOT_FOUND = "Product with id {} not found"  
INSUFFICIENT_STOCK = "Not enough stock for product {}"  
NO_ORDERS_FOUND = "No orders found for this user"  
BILL_NOT_FOUND = "Bill not found for this order"  
ORDER_DELETE_FORBIDDEN = "Cannot delete order: bill is already confirmed or processed."  
ORDER_DELETED = "Order deleted successfully."  
BASE_URL = "http://127.0.0.1:8000"  
PENDING = "Pending"  
  
def get_product_or_404(db: Session, product_id: int):  
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()  
    if not product:  
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=PRODUCT_NOT_FOUND.format(product_id))  
    return product  
  
def get_order_or_404(db: Session, order_id: int, user_id: int):  
    order = db.query(models.Order).filter(models.Order.order_id == order_id, models.Order.user_id == user_id).first()  
    if not order:  
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=ORDER_NOT_FOUND)  
    return order  
  
def get_bill_or_404(db: Session, order_id: int):  
    bill = db.query(models.Bill).filter(models.Bill.order_id == order_id).first()  
    if not bill:  
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=BILL_NOT_FOUND)  
    return bill  
  
def get_order_items_details(db: Session, order_id: int):  
    items = (  
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
        for order_item, product, brand in items  
    ]  
  
@router.post("/orders", response_model=schemas.OrderOut)  
async def create_order(  
    order: schemas.OrderCreate,  
    db: Session = Depends(get_db),  
    current_user: models.User = Depends(get_current_user),  
):  
    db_order = models.Order(user_id=current_user.user_id, status=PENDING)  
    db.add(db_order)  
    db.commit()  
    db.refresh(db_order)  
  
    total_amount = Decimal(0)  
    for item in order.order_items:  
        product = get_product_or_404(db, item.product_id)  
  
        if product.order_quantity is not None and item.quantity > product.order_quantity:  
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=INSUFFICIENT_STOCK.format(product.product_name))  
  
        item_cost = Decimal(product.price) * item.quantity  
        total_amount += item_cost  
  
        db_order_item = models.OrderItem(  
            order_id=db_order.order_id,  
            product_id=item.product_id,  
            size=item.size,  
            quantity=item.quantity,  
        )  
        db.add(db_order_item)  
  
    bill = models.Bill(  
        order_id=db_order.order_id,  
        amount=total_amount,  
        method=PENDING,  
        trx_id="1234",  
        status=PENDING,  
    )  
    db.add(bill)  
    db.commit()  
    db.refresh(db_order)  
    return db_order  
  
def place_order(user_id, product_id, size, quantity=1):  
    session = SessionLocal()  
    try:  
        product = (  
            session.query(models.Product)  
            .filter(models.Product.product_id == product_id, models.Product.order_size == size)  
            .first()  
        )  
        if not product:  
            return PRODUCT_NOT_FOUND.format(product_id)  
  
        if product.order_quantity < quantity:  
            return INSUFFICIENT_STOCK.format(product.product_name)  
  
        new_order = models.Order(  
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
  
  
  
 
@router.get("/orders/me/details", response_model=List[schemas.OrderDetailOut])  
async def get_my_orders_details(  
    db: Session = Depends(get_db),  
    current_user: models.User = Depends(get_current_user),  
):  
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.user_id).all()  
    if not orders:  
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No orders found for this user")  
  
    orders_details = []  
    for order in orders:  
        bill = db.query(models.Bill).filter(models.Bill.order_id == order.order_id).first()  
        order_items = (  
            db.query(models.OrderItem, models.Product, models.Brand)  
            .join(models.Product, models.OrderItem.product_id == models.Product.product_id)  
            .join(models.Brand, models.Product.brand_id == models.Brand.brand_id)  
            .filter(models.OrderItem.order_id == order.order_id)  
            .all()  
        )  
  
        items_details = [  
            {  
                "product_id": product.product_id,  
                "brand_id": brand.brand_id,  
                "product_name": product.product_name,  
                "brand_name": brand.brand_name,  
                "order_size": order_item.size,  
                "order_quantity": order_item.quantity,  
            }  
            for order_item, product, brand in order_items  
        ]  
  
        order_data = {  
            "order_id": order.order_id,  
            "status": order.status,  
            "bill_status": bill.status if bill else None,  
            "created_at": order.created_at,  
            "bill_amount": bill.amount if bill else None,  
            "order_items": items_details,  
        }  
        orders_details.append(order_data)  
  
    return orders_details  


@router.get("/orders/me")  
async def get_my_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):  
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.user_id).all()  
    if not orders:  
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NO_ORDERS_FOUND)  
  
    return [  
        {  
            "order_id": order.order_id,  
            "user_id": order.user_id,  
            "status": order.status,  
            "order_details_url": f"{BASE_URL}/order/{order.order_id}",  
            "product_details_url": f"{BASE_URL}/order/{order.order_id}/products",  
        }  
        for order in orders  
    ]  
  
@router.get("/orders/{order_id}/bill", response_model=schemas.BillOut)  
async def get_bill_for_order(  
    order_id: int,  
    db: Session = Depends(get_db),  
    current_user: models.User = Depends(get_current_user),  
):  
    order = get_order_or_404(db, order_id, current_user.user_id)  
    bill = get_bill_or_404(db, order.order_id)  
    return bill  
  
@router.get("/orders/{order_id}/details", response_model=schemas.OrderDetailOut)  
async def get_order_details(  
    order_id: int,  
    db: Session = Depends(get_db),  
    current_user: models.User = Depends(get_current_user),  
):  
    order = get_order_or_404(db, order_id, current_user.user_id)  
    bill = get_bill_or_404(db, order.order_id)  
    order_items = get_order_items_details(db, order.order_id)  
  
    return {  
        "order_id": order.order_id,  
        "status": order.status,  
        "created_at": order.created_at,  
        "bill_amount": bill.amount if bill else None,  
        "order_items": order_items,  
    }  

@router.delete("/orders/{order_id}")  
async def delete_order(  
    order_id: int,  
    db: Session = Depends(get_db),  
    current_user: models.User = Depends(get_current_user),  
):  
    order = get_order_or_404(db, order_id, current_user.user_id)  
    bill = get_bill_or_404(db, order.order_id)  
  
    if bill.status.lower() != PENDING.lower():  
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=ORDER_DELETE_FORBIDDEN)  
  
    db.delete(order)  
    db.commit()  
    return {"detail": ORDER_DELETED}  