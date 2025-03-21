import os
from dotenv import load_dotenv
from langchain_core import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")

# Initialize Azure OpenAI client
llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    temperature=0.5,
)

# System prompt for the AI agent
SYSTEM_PROMPT = """
You are an AI shopping assistant for an e-commerce platform. Your job is to:
1. Help users find products they're looking for based on their descriptions
2. Assist users in placing orders for products they select

When helping users find products:
- Extract relevant search criteria from their query (product type, features, price range, etc.)
- Present matching products in a clear, organized manner
- Allow users to compare options and make selections

When placing orders:
- Capture required information: product ID, size (if applicable), quantity, and shipping details
- Confirm order details before submission
- Provide order confirmation and next steps

Be conversational, helpful, and concise in your responses.
"""

# Create the chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])