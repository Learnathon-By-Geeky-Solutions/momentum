# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from user_management.schemas import ChatRequest, ChatResponse
# from user_management.ai.llm import process_ai_request_with_langchain
# from user_management.database import get_db

# router = APIRouter()


# @router.post("/agent", response_model=ChatResponse)
# def chat_with_ai(chat_request: ChatRequest, db: Session = Depends(get_db)):
#     user_message = " ".join(chat_request.messages)
#     response_text = process_ai_request_with_langchain(user_message, db)
#     return {"response": response_text}
