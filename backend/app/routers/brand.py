from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.schemas as schemas
import app.models as models
from app.models import User, Brand
from app.utils import (
    get_current_user,
)
from typing import List, Optional

from fastapi import APIRouter


router = APIRouter()


@router.get("/brands")
async def get_brands(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    brands = db.query(models.Brand).offset(skip).limit(limit).all()
    return brands



@router.post("/brands", response_model=schemas.BrandOut)
async def create_brand(
    brand: schemas.BrandCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    existing_brand = (
        db.query(models.Brand).filter(models.Brand.user_id == user.user_id).first()
    )

    if existing_brand:
        raise HTTPException(status_code=400, detail="You can create only one brand.")

    if user.role == "customer":
        raise HTTPException(status_code=400, detail="Need to register as Artisan. ")

    new_brand = models.Brand(
        user_id=user.user_id,
        brand_name=brand.brand_name,
        brand_description=brand.brand_description,
        logo=brand.logo,
    )
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand


@router.get("/brands/me", response_model=schemas.BrandOut)
async def get_my_brand(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    brand = (
        db.query(models.Brand)
        .filter(models.Brand.user_id == current_user.user_id)
        .first()
    )

    if not brand:
        raise HTTPException(status_code=404, detail="You have not created a brand")

    return brand


@router.patch("/brands/me", response_model=schemas.BrandOut)
async def update_brand(
    brand: schemas.BrandCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_brand = (
        db.query(models.Brand)
        .filter(models.Brand.user_id == current_user.user_id)
        .first()
    )

    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    update_data = brand.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_brand, key, value)

    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.get("/brands/{brand_id}")
async def get_brand(
    brand_id: int,
    db: Session = Depends(get_db),
):
    brand = db.query(models.Brand).filter(models.Brand.brand_id == brand_id).first()

    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    products = (
        db.query(models.Product).filter(models.Product.brand_id == brand_id).all()
    )
    brand.products = products

    return brand
