from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import Order, Product, Bill
from app import models

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
    product = (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )
    if not product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=PRODUCT_NOT_FOUND.format(product_id)
        )
    return product


def get_order_or_404(db: Session, order_id: int, user_id: int):
    order = (
        db.query(models.Order)
        .filter(models.Order.order_id == order_id, models.Order.user_id == user_id)
        .first()
    )
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


def get_user_brand_ids(db: Session, user_id: int) -> list:
    """Get all brand IDs belonging to a user"""
    user_brands = db.query(models.Brand).filter(models.Brand.user_id == user_id).all()
    if not user_brands:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No brands found for this user"
        )

    return [brand.brand_id for brand in user_brands]


def validate_artisan_order_access(
    db: Session, order_id: int, brand_ids: list
) -> models.Order:
    """Validate that an order contains products from the artisan's brands"""
    order_has_user_products = (
        db.query(models.Order)
        .filter(
            models.Order.order_id == order_id,
            models.Order.order_id.in_(
                db.query(models.OrderItem.order_id)
                .join(
                    models.Product,
                    models.OrderItem.product_id == models.Product.product_id,
                )
                .filter(models.Product.brand_id.in_(brand_ids))
            ),
        )
        .first()
    )

    if not order_has_user_products:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Order not found or does not contain your products",
        )

    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    return order


def get_artisan_order_items(db: Session, order_id: int, brand_ids: list) -> list:
    """Get order items that belong to the artisan's brands"""
    order_items = (
        db.query(models.OrderItem, models.Product, models.Brand)
        .join(models.Product, models.OrderItem.product_id == models.Product.product_id)
        .join(models.Brand, models.Product.brand_id == models.Brand.brand_id)
        .filter(
            models.OrderItem.order_id == order_id,
            models.Product.brand_id.in_(brand_ids),
        )
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
        for order_item, product, brand in order_items
    ]


def format_order_response(order):
    """Format the order response object"""
    return {
        "order_id": order.order_id,
        "user_id": order.user_id,
        "status": order.status,
        "order_details_url": f"{BASE_URL}/order/{order.order_id}",
        "product_details_url": f"{BASE_URL}/order/{order.order_id}/products",
    }
