from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Product, Brand
from app.ai.utils.ai_search import (
    detect_language,
    generate_keywords,
    get_most_similar_products,
)

router = APIRouter()

@router.get("/")
def ai_product_search(
    q: str = Query(..., description="Search query (Bangla/English)"),
    db: Session = Depends(get_db),
):
    lang = detect_language(q)
    search_data = generate_keywords(q)

    keywords_original = search_data.get("keywords", [])
    keywords_en = search_data.get("keywords_en", [])
    synonyms = search_data.get("synonyms", {})
    category = search_data.get("category")
    price_range = search_data.get("price_range")
    brand_name = search_data.get("brand")

    print("Extracted AI original keywords:", keywords_original)
    print("Extracted AI English translated keywords:", keywords_en)

    query = db.query(Product).filter(Product.approved == True)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if price_range and isinstance(price_range, list) and len(price_range) == 2:
        min_price, max_price = price_range
        if min_price is not None and max_price is not None:
            query = query.filter(Product.price >= min_price, Product.price <= max_price)
    if brand_name:
        query = query.join(Brand).filter(Brand.brand_name.ilike(f"%{brand_name}%"))

    all_products = query.all()
    print(f"Total products fetched from DB: {len(all_products)}")

    
    matched_products = get_most_similar_products(all_products, keywords_en, synonyms)

    return {
        "language": lang,
        "keywords_used": keywords_en or keywords_original,
        "total_found": len(matched_products),
        "products": [
            {
                "product_id": p.product_id,
                "name": p.product_name,
                "category": p.category,
                "price": str(p.price),
                "description": p.description,
                "images": p.product_pic,
                "videos": p.product_video,
            }
            for p in matched_products
        ],
    }
