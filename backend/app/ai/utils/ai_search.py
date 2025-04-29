from openai import AzureOpenAI
from langdetect import detect
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from rapidfuzz import fuzz
import os
import json
import re
from typing import List, Union, Dict, Any

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


def generate_keywords(query: str) -> Dict[str, Any]:
    prompt = f"""Extract product search filters and translate to English clearly from the user's input below.
      
User input: "{query}"  
Respond ONLY in valid JSON format clearly with this structure:  
{{  
  "keywords": [list of main product words in original language],  
  "keywords_en": [list of main product keywords translated clearly to English],  
  "category": string or null,  
  "price_range": [min, max] or null,  
  "brand": string or null,
  "synonyms": {{ keyword: [synonym1, synonym2] }}  # Added synonyms
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
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
        print("Generated response:", text)
        json_text = re.search(r"{.*}", text, re.DOTALL)
        if json_text:
            return json.loads(json_text.group())
        else:
            return {"keywords": [], "keywords_en": [], "synonyms": {}}
    except (json.JSONDecodeError, AttributeError, IndexError) as e:
        print(f"Error parsing AI response: {e}")
        return {"keywords": [], "keywords_en": [], "synonyms": {}}


def extract_price_range_from_text(text: str) -> Union[List[float], None]:
    text = text.lower()

    match_under = re.search(r"under\s*(\d+)", text)
    if match_under:
        max_price = float(match_under.group(1))
        return [0, max_price]

    match_below = re.search(r"below\s*(\d+)", text)
    if match_below:
        max_price = float(match_below.group(1))
        return [0, max_price]

    match_between = re.search(r"between\s*(\d+)\s*and\s*(\d+)", text)
    if match_between:
        min_price = float(match_between.group(1))
        max_price = float(match_between.group(2))
        return [min_price, max_price]

    match_from_to = re.search(r"from\s*(\d+)\s*to\s*(\d+)", text)
    if match_from_to:
        min_price = float(match_from_to.group(1))
        max_price = float(match_from_to.group(2))
        return [min_price, max_price]

    return None


def get_most_similar_products(products, keywords, synonyms):
    keyword_texts = []

    for keyword in keywords:
        keyword_texts.append(keyword.lower())

        if keyword in synonyms:
            for synonym in synonyms[keyword]:
                keyword_texts.append(synonym.lower())

    print(f"Enhanced Keywords for Search (including synonyms): {keyword_texts}")

    matched_products = [
        product
        for product in products
        if any(
            keyword
            in (
                f"{product.product_name or ''} {product.category or ''} {product.description or ''}"
            ).lower()
            for keyword in keyword_texts
        )
    ]

    if matched_products:
        return matched_products

    fuzzy_threshold = 68
    fuzzy_matches = [
        (
            product,
            fuzz.partial_ratio(
                " ".join(keyword_texts),
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
