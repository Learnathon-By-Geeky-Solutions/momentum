import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Azure OpenAI Configuration
openai.api_type = "azure"
openai.api_base = os.getenv("API_BASE")
openai.api_version = os.getenv("API_VERSION")
openai.api_key = os.getenv("API_KEY")

# Azure Deployment Name (NOT the model name, but the deployment name set in Azure)
DEPLOYMENT_NAME = "gpt-4o-3"


def get_conversational_response(messages: list, user_id) -> str:
    """
    Processes user messages to search for products or place orders.
    """
    user_message = messages[-1]["content"].lower()

    # If the user is searching for a t-shirt
    if "t-shirt" in user_message or "tshirt" in user_message or "shirt" in user_message:
        return get_matching_products("t-shirt")

    # Detect "Select {product_id} {size}" command for ordering
    if user_message.startswith("select"):
        try:
            parts = user_message.split(" ")
            product_id = int(parts[1])
            size = parts[2] if len(parts) > 2 else None  # Extract size if provided
            return place_order(user_id, product_id, size)
        except:
            return "Invalid order command. Use 'Select {product_id} {size}' to place an order."

    # Otherwise, continue conversation with OpenAI
    try:
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME, messages=messages, temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"LLM API error: {e}"
