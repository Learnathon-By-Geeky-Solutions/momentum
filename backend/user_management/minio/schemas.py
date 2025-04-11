from pydantic import BaseModel
from typing import List


class ProductPhotoUploadResponse(BaseModel):
    message: str
    urls: List[str]


class ProductVideoUploadResponse(BaseModel):
    message: str
    urls: List[str]
