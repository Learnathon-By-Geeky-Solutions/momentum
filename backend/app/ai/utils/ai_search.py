# utils/ai_search.py
from openai import AzureOpenAI
from langdetect import detect
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from rapidfuzz import fuzz
import os
import json
import re

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"


def generate_keywords(query: str) -> dict:
    prompt = f"""Extract product search filters and translate to English clearly from the user's input below.  
User input: "{query}"  
Respond ONLY in valid JSON format clearly with this structure:  
{{  
  "keywords": [list of main product words in original language],  
  "keywords_en": [list of main product words translated clearly to English],  
  "category": string or null,  
  "price_range": [min, max] or null,  
  "brand": string or null  
}}"""

    response = client.chat.completions.create(
        model="gpt-4.5-preview",
        temperature=0.5,
        messages=[
            {
                "role": "system",
                "content": "You're a helpful product search assistant and translator.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    try:
        text = response.choices[0].message.content
        json_text = re.search(r"{.*}", text, re.DOTALL)
        if json_text:
            return json.loads(json_text.group())
        else:
            return {"keywords": [], "keywords_en": []}
    except Exception:
        return {"keywords": [], "keywords_en": []}


def get_most_similar_products(products, keywords):
    keyword_text = " ".join(keywords).lower().strip()
    matched_products = [
        product
        for product in products
        if keyword_text
        in (
            f"{product.product_name or ''} {product.category or ''} {product.description or ''}"
        ).lower()
    ]
    if matched_products:
        return matched_products

    fuzzy_threshold = 68
    fuzzy_matches = [
        (
            product,
            fuzz.partial_ratio(
                keyword_text,
                (
                    f"{product.product_name or ''} {product.category or ''} {product.description or ''}"
                ).lower(),
            ),
        )
        for product in products
    ]
    fuzzy_matches = sorted(
        [(p, score) for p, score in fuzzy_matches if score >= fuzzy_threshold],
        key=lambda x: x[1],
        reverse=True,
    )
    return [p for p, _ in fuzzy_matches]
