from fastapi import APIRouter, Depends, HTTPException, Body
from user_management.schemas import ChatRequest, ChatResponse, OrderCreate

from sqlalchemy.orm import Session
from user_management.utils import get_current_user
from user_management.database import get_db
from user_management.routers.order import create_order
from user_management.ai.llm import get_conversational_response
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, current_user=Depends(get_current_user)):
    """
    Conversational endpoint:
    Accepts a user message and returns a response generated by the LLM.
    """
    # Build conversation context. In a real system, you might store conversation history.
    messages = [
        {"role": "system", "content": "You are a helpful product ordering assistant."},
        {"role": "user", "content": request.message}
    ]
    try:
        answer = get_conversational_response(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return ChatResponse(response=answer)




@router.post("/agent/order")
async def agent_create_order(
    conversation: list = Body(...),  # The conversation history (list of messages)
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    A combined endpoint that takes a conversation history,
    uses the LLM to decide on order details, and creates an order.
    In a real system, you might use the conversation context to ask:
      - Which product to order?
      - How many?
      - What size?
    For demonstration, we assume the LLM returns a JSON string with order details.
    """
    try:
        llm_response = get_conversational_response(conversation)
        # Assume the LLM response is a JSON string containing order details:
        # e.g., {"product_id": 123, "quantity": 2, "size": "L"}
        import json
        order_data = json.loads(llm_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing conversation: {str(e)}")
    
    # Create an order using the extracted order_data
    order_create = OrderCreate(**order_data)
    new_order = create_order(order_create, db=db, current_user=current_user)
    return new_order