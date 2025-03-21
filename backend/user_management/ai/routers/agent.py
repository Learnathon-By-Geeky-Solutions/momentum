from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from database import get_db
from models import User
from ai.agent_schema import ChatRequest, ChatResponse
from ai.agent_service import AgentService

router = APIRouter()

# Store chat histories in memory (in production, use a database)
chat_histories = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # Get or initialize chat history
    user_id = request.user_id
    session_id = f"user_{user_id}" if user_id else "anonymous"
    
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    
    chat_history = chat_histories[session_id]
    user_message = request.messages[-1]  # Get the last message from the user
    
    # Initialize the agent service
    agent_service = AgentService(db)
    
    # Process the message
    response, search_results, order_result = agent_service.process_message(
        user_message=user_message,
        chat_history=chat_history,
        user_id=user_id
    )
    
    # Update the chat history
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": response})
    
    # Limit chat history size
    if len(chat_history) > 20:
        chat_history = chat_history[-20:]
    
    chat_histories[session_id] = chat_history
    
    return ChatResponse(
        response=response,
        product_results=search_results,
        order_result=order_result
    )

@router.post("/order-product")
async def order_product(
    user_id: int,
    product_id: int,
    quantity: int,
    size: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Initialize the agent service
    agent_service = AgentService(db)
    
    # Use the order tool directly
    tools = agent_service.tools
    result = tools.create_order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        size=size
    )
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result