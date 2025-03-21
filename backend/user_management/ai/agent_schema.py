from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ProductSearchQuery(BaseModel):
    query: str = Field(..., description="The search query for finding products")

class ProductRequest(BaseModel):
    product_id: int = Field(..., description="The ID of the product to get details for")

class OrderRequest(BaseModel):
    user_id: int = Field(..., description="The ID of the user placing the order")
    product_id: int = Field(..., description="The ID of the product being ordered")
    quantity: int = Field(..., description="The quantity of the product being ordered")
    size: Optional[str] = Field(None, description="Optional size selection for the product")

class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (user or assistant)")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    messages: List[str] = Field(..., description="The list of chat messages in the conversation")
    user_id: Optional[int] = Field(None, description="The ID of the user in the conversation, if authenticated")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The response from the AI assistant")
    product_results: Optional[List[Dict[str, Any]]] = Field(None, description="Optional product search results")
    order_result: Optional[Dict[str, Any]] = Field(None, description="Optional order creation result")
    
class AgentState(BaseModel):
    chat_history: List[ChatMessage] = Field(default_factory=list)
    search_results: Optional[List[Dict[str, Any]]] = None
    selected_product: Optional[Dict[str, Any]] = None
    order_details: Optional[Dict[str, Any]] = None
    stage: str = "initial"  # Can be: initial, searching, selection, ordering, confirmation