from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from user_management import schemas, models
from user_management.database import get_db  # Database session dependency
from user_management.models import User, Product, Brand, Order, OrderItem  # ORM models
from user_management.utils import get_current_user
from user_management.schemas import ProductCreate, ProductOut  # Pydantic schemas
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from user_management.database import get_db
from fastapi import APIRouter


router = APIRouter()


# Post Product (protected route)
@router.post("/products", response_model=schemas.ProductCreate)
def post_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    current_user: models.User = Depends(get_current_user),
):

    brand = (
        db.query(models.Brand)
        .filter(models.Brand.user_id == current_user.user_id)
        .first()
    )
    print(brand.brand_id)

    if not brand:
        raise HTTPException(status_code=400, detail="Brand does not exist.")
    if brand.user_id != user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to add products to this brand.",
        )

    new_product = models.Product(
        brand_id=brand.brand_id,
        product_name=product.product_name,
        product_pic=product.product_pic,
        product_video=product.product_video,
        category=product.category,
        description=product.description,
        order_size=product.order_size,
        order_quantity=product.order_quantity,
        quantity_unit=product.quantity_unit,
        price=product.price,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/products/{product_id}", response_model=schemas.ProductCreate)
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    # Update product fields
    product.product_name = updated_product.product_name
    product.product_pic = updated_product.product_pic
    product.product_video = updated_product.product_video
    product.category = updated_product.category
    product.description = updated_product.description
    product.order_size = updated_product.order_size
    product.order_quantity = updated_product.order_quantity
    product.quantity_unit = updated_product.quantity_unit
    product.price = updated_product.price

    db.commit()
    db.refresh(product)
    return product


@router.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return product


@router.get("/products", response_model=List[schemas.ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Retrieve the product by its ID
    product = (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Retrieve the brand associated with the product
    brand = (
        db.query(models.Brand).filter(models.Brand.brand_id == product.brand_id).first()
    )
    # Ensure the current user owns this brand
    if not brand or brand.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this product"
        )

    # Check for any pending order items for this product.
    # This joins OrderItem and Order, and checks if there is any order with status "Pending"
    pending_order_item = (
        db.query(models.OrderItem)
        .join(models.Order, models.OrderItem.order_id == models.Order.order_id)
        .filter(
            models.OrderItem.product_id == product_id, models.Order.status == "Pending"
        )
        .first()
    )

    if pending_order_item:
        raise HTTPException(
            status_code=400, detail="Complete the order before deleting this product."
        )

    # If no pending order is found, delete the product.
    db.delete(product)
    db.commit()

    return {"detail": "Product deleted successfully."}


def get_matching_products(query):
    """
    Searches the product table for relevant items.
    """
    session = SessionLocal()
    try:
        # Search for products matching query in name, category, or description
        products = (
            session.query(Product)
            .filter(
                (Product.product_name.ilike(f"%{query}%"))
                | (Product.category.ilike(f"%{query}%"))
                | (Product.description.ilike(f"%{query}%"))
            )
            .limit(5)
            .all()
        )

        if not products:
            return "No matching products found."

        response_text = "**Here are the available t-shirts in our collection:**\n\n"
        for product in products:
            response_text += (
                f"**{product.product_name}**\n"
                f"📝 {product.description}\n"
                f"💲 Price: ${product.price}\n"
                f"📦 Available Sizes: {product.order_size}\n"
                f"📏 Quantity Unit: {product.quantity_unit}\n"
                f"⭐ Rating: {product.rating or 'N/A'}\n"
                f"🖼️ Images: {', '.join(product.product_pic) if product.product_pic else 'No images available'}\n"
                f"📽️ Videos: {', '.join(product.product_video) if product.product_video else 'No videos available'}\n"
                f"🛒 *Reply with 'Select {product.product_id} {product.order_size}' to place an order.*\n\n"
            )

        return response_text

    finally:
        session.close()
