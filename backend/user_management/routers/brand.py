
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from user_management.database import get_db
from user_management import schemas
from user_management.models import User, Brand
from user_management.schemas import BrandCreate, BrandOut
from user_management.utils import get_current_user  # Adjust the path based on your project structure
from typing import List, Optional

from fastapi import APIRouter

import user_management.models as models

router = APIRouter()







# Create Brand (protected route)
@router.post("/create-brand", response_model=schemas.BrandOut)
async def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    
    
    existing_brand = db.query(models.Brand).filter(models.Brand.user_id == user.user_id).first()

    #print(existing_brand.brand_name)
    
    if existing_brand:
        raise HTTPException(status_code=400, detail="You can create only one brand.")


    new_brand = models.Brand(
        user_id=user.user_id,
        brand_name=brand.brand_name,
        brand_description=brand.brand_description,
        logo=brand.logo
    )
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand


@router.get("/brands/me", response_model=schemas.BrandOut)
async def get_my_brand(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    brand = db.query(models.Brand).filter(models.Brand.user_id == current_user.user_id).first()
    
    if not brand:
        raise HTTPException(status_code=404, detail="You have not created a brand")
    
    return brand



@router.put("/updatebrands/me", response_model=schemas.BrandOut)
async def update_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    

    db_brand = db.query(models.Brand).filter(models.Brand.user_id == current_user.user_id).first()
    
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    db_brand.brand_name = brand.brand_name
    db_brand.brand_description = brand.brand_description
    db_brand.logo = brand.logo

    db.commit()
    db.refresh(db_brand)
    return db_brand
