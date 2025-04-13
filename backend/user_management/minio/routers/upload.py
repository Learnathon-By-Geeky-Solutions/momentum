from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Product
from app.minio.utils import upload_to_minio
from app.minio.schemas import (
    ProductPhotoUploadResponse,
    ProductVideoUploadResponse,
)

router = APIRouter()


@router.post("/upload/photos/{product_id}", response_model=ProductPhotoUploadResponse)
async def upload_photos(
    product_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    urls = [await upload_to_minio(file, "photos") for file in files]
    product.product_pic = urls  # Store URLs in PostgreSQL
    db.commit()
    return {"message": "Photos uploaded successfully", "urls": urls}


@router.post("/upload/videos/{product_id}", response_model=ProductVideoUploadResponse)
async def upload_videos(
    product_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    urls = [await upload_to_minio(file, "videos") for file in files]
    product.product_video = urls  # Store URLs in PostgreSQL
    db.commit()
    return {"message": "Videos uploaded successfully", "urls": urls}
