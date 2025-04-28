from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import app.schemas as schemas
import app.models as models
from app.database import get_db  # Database session dependency
from app.models import User, Product, Brand, Order, OrderItem  # ORM models
from app.utils import get_current_user
from app.schemas import ProductCreate, ProductOut  # Pydantic schemas
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
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

@router.get("/products/me", response_model=List[schemas.ProductOut])
def get_products_me(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    products = (
        db.query(models.Product)
       .join(models.Brand, models.Product.brand_id == models.Brand.brand_id)
       .filter(models.Brand.user_id == user.user_id)
       .all()
    )
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this user.")
    return products 
    

@router.patch("/products/{product_id}", response_model=schemas.ProductCreate)
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

    update_data = updated_product.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

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

    product = (
        db.query(models.Product).filter(models.Product.product_id == product_id).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    brand = (
        db.query(models.Brand).filter(models.Brand.brand_id == product.brand_id).first()
    )

    if not brand or brand.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this product"
        )

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

    db.delete(product)
    db.commit()

    return {"detail": "Product deleted successfully."}
