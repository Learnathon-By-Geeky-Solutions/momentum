from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from typing import List, Tuple, Optional
from user_management.minio.utils import upload_to_minio
from user_management.minio.schemas import ProductPhotoUploadResponse, SimpleResponse
from user_management.utils import get_current_user  # Updated auth dependency
from user_management.models import User, Product
from user_management.minio.utils import validate_file_type, validate_file_size, VALID_TYPES, delete_from_minio, extract_minio_object_key, validate_files
from user_management.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import any_

PRODUCT_VIDEO = "product video"
PRODUCT_PHOTO = "product photo"

def get_folder_for_type(upload_type: str) -> str:
    if upload_type == "profile":
        return "profile"
    if upload_type == PRODUCT_PHOTO:
        return "photos"
    return "videos"

router = APIRouter()


@router.post("/upload", response_model=ProductPhotoUploadResponse)
async def unified_upload(
    upload_type: str = Form(...),
    files: List[UploadFile] = File(...),
    user: User = Depends(get_current_user)  # Require user login
):
    if upload_type.lower() not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {', '.join(VALID_TYPES)}")

    upload_type = upload_type.lower()

    for file in files:
        content_type = file.content_type
        contents = await file.read()
        file_size = len(contents)
        await file.seek(0)  # Reset file pointer after reading

        validate_file_type(content_type, upload_type)
        validate_file_size(file_size)

    folder = get_folder_for_type(upload_type)
    urls = [await upload_to_minio(file, folder) for file in files]

    return {"message": f"{upload_type.capitalize()} uploaded successfully", "urls": urls}




@router.patch("/upload", response_model=ProductPhotoUploadResponse)
async def update_uploaded_files(
    upload_type: str = Form(...),
    files: List[UploadFile] = File(...),
    user: User = Depends(get_current_user)
):
    upload_type = upload_type.lower()
    if upload_type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {', '.join(VALID_TYPES)}")

    validate_files(files, upload_type)

    folder_map = {
        "profile": "profile",
        PRODUCT_PHOTO: "photos",
        PRODUCT_VIDEO: "videos"
    }
    folder = folder_map[upload_type]

    urls = [await upload_to_minio(file, folder) for file in files]

    return {"message": f"{upload_type.capitalize()} updated successfully", "urls": urls}

def find_product_and_url(products: List[Product], product_field: str, file_name: str) -> Tuple[Optional[Product], Optional[str]]:
    for product in products:
        file_urls = getattr(product, product_field, [])
        for url in file_urls:
            if file_name in url:
                return product, url
    return None, None

@router.delete("/upload/{upload_type}/{file_name}", response_model=ProductPhotoUploadResponse)
async def delete_uploaded_file(
    upload_type: str,
    file_name: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    upload_type = upload_type.lower()

    if upload_type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {', '.join(VALID_TYPES)}")

    product_field_map = {
        PRODUCT_PHOTO: "product_pic",
        PRODUCT_VIDEO: "product_video"
    }

    product_field = product_field_map.get(upload_type)

    if product_field:
        products = db.query(Product).all()
        target_product, target_file_url = find_product_and_url(products, product_field, file_name)

        if not target_product or not target_file_url:
            raise HTTPException(status_code=404, detail=f"File '{file_name}' not found in the database.")

        updated_files = [f for f in getattr(target_product, product_field) if f != target_file_url]
        setattr(target_product, product_field, updated_files)
        db.commit()

        minio_key = extract_minio_object_key(target_file_url)
        success = await delete_from_minio(minio_key)

        if not success:
            raise HTTPException(status_code=404, detail=f"File '{target_file_url}' not found in MinIO")

        return {
            "message": f"{upload_type.capitalize()} file '{file_name}' deleted successfully",
            "urls": [target_file_url]
        }

    raise HTTPException(status_code=400, detail="Unsupported upload type for deletion.")