from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from typing import List
from user_management.minio.utils import upload_to_minio
from user_management.minio.schemas import ProductPhotoUploadResponse, SimpleResponse
from user_management.utils import get_current_user  # Updated auth dependency
from user_management.models import User, Product
from user_management.minio.utils import validate_file_type, validate_file_size, VALID_TYPES, delete_from_minio, extract_minio_object_key
from user_management.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import any_




router = APIRouter()




VALID_TYPES = ["profile", "product photo", "product video"]
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/mpeg"]
MAX_FILE_SIZE_MB = 5  # 5 MB

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

    folder = "profile" if upload_type == "profile" else "photos" if upload_type == "product photo" else "videos"
    urls = [await upload_to_minio(file, folder) for file in files]

    return {"message": f"{upload_type.capitalize()} uploaded successfully", "urls": urls}



def validate_files(files: List[UploadFile], file_type: str):
    for file in files:
        content_type = file.content_type
        contents = file.file.read()
        file_size = len(contents)
        file.file.seek(0)

        if file_type in ["profile", "product photo"] and content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid image file type: {content_type}")
        if file_type == "product video" and content_type not in ALLOWED_VIDEO_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid video file type: {content_type}")
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE_MB}MB")


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
        "product photo": "photos",
        "product video": "videos"
    }
    folder = folder_map[upload_type]

    urls = [await upload_to_minio(file, folder) for file in files]

    return {"message": f"{upload_type.capitalize()} updated successfully", "urls": urls}

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

    folder_map = {
        "profile": "profile",
        "product photo": "photos",
        "product video": "videos"
    }
    product_field_map = {
        "product photo": "product_pic",
        "product video": "product_video"
    }

    folder = folder_map[upload_type]
    product_field = product_field_map.get(upload_type)

    if product_field:
        # Look for the product containing this file_name in its URL
        products = db.query(Product).all()
        target_product = None
        target_file_url = None

        for product in products:
            file_urls = getattr(product, product_field, [])
            for url in file_urls:
                if file_name in url:
                    target_product = product
                    target_file_url = url
                    break
            if target_product:
                break

        if not target_product or not target_file_url:
            raise HTTPException(status_code=404, detail=f"File '{file_name}' not found in the database.")

        # Remove the file URL from the DB
        updated_files = [f for f in getattr(target_product, product_field) if f != target_file_url]
        setattr(target_product, product_field, updated_files)
        db.commit()

        # Convert URL to MinIO key like 'photos/007.jpg'
        minio_key = extract_minio_object_key(target_file_url)
        success = await delete_from_minio(minio_key)


        if not success:
            raise HTTPException(status_code=404, detail=f"File '{target_file_url}' not found in MinIO")

        return {
            "message": f"{upload_type.capitalize()} file '{file_name}' deleted successfully",
            "urls": [target_file_url]
        }

    raise HTTPException(status_code=400, detail="Unsupported upload type for deletion.")
