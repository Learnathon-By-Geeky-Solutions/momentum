from typing import Dict, List, Tuple, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from sqlalchemy.orm import Session
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import StrOutputParser

from ai.agent_config import llm, chat_prompt
from ai.agent_tools import AgentTools
from ai.agent_schema import AgentState, ChatMessage

class AgentService:
    def __init__(self, db: Session):
        self.db = db
        self.tools = AgentTools(db)
        self.chain = self._build_chain()
        self.graph = self._build_graph()
    
    def _build_chain(self):
        # Build the basic conversation chain
        return chat_prompt | llm | StrOutputParser()
    
    def _build_graph(self):
        # Build the state graph for the agent workflow
        workflow = StateGraph(AgentState)
        
        # Define the nodes
        workflow.add_node("process_input", self._process_input)
        workflow.add_node("search_products", self._search_products)
        workflow.add_node("provide_product_details", self._provide_product_details)
        workflow.add_node("create_order", self._create_order)
        workflow.add_node("generate_response", self._generate_response)
        
        # Define the edges
        workflow.add_edge("process_input", "search_products")
        workflow.add_edge("search_products", "provide_product_details")
        workflow.add_edge("provide_product_details", "create_order")
        workflow.add_edge("create_order", "generate_response")
        workflow.add_edge("generate_response", END)
        
        # Set the entry point
        workflow.set_entry_point("process_input")
        
        return workflow.compile()
    
    def _process_input(self, state: AgentState) -> Dict[str, Any]:
        # Analyze the user input to determine intent
        last_message = state.chat_history[-1].content if state.chat_history else ""
        
        # Check if input contains a product search intent
        search_keywords = ["find", "search", "looking for", "show me", "want to buy"]
        if any(keyword in last_message.lower() for keyword in search_keywords):
            state.stage = "searching"
            return {"stage": "searching"}
        
        # Check if input contains a product selection intent
        selection_keywords = ["select", "choose", "want this", "product id", "buy this", "order this"]
        if any(keyword in last_message.lower() for keyword in selection_keywords):
            state.stage = "selection"
            return {"stage": "selection"}
        
        # Check if input contains an order intent
        order_keywords = ["place order", "buy now", "checkout", "order now", "purchase"]
        if any(keyword in last_message.lower() for keyword in order_keywords):
            state.stage = "ordering"
            return {"stage": "ordering"}
        
        # Default to searching
        state.stage = "searching"
        return {"stage": "searching"}
    
    def _search_products(self, state: AgentState) -> Dict[str, Any]:
        # Extract the search query from the last message
        query = state.chat_history[-1].content
        
        # Use the search_products tool
        search_results = self.tools.search_products(query)
        state.search_results = search_results
        
        if not search_results:
            # No products found, generate a response
            state.stage = "generate_response"
            return {"stage": "generate_response"}
        
        # Move to the product selection stage
        state.stage = "selection"
        return {"stage": "selection"}
    
    def _provide_product_details(self, state: AgentState) -> Dict[str, Any]:
        # Try to extract a product_id from the user message
        message = state.chat_history[-1].content
        import re
        
        # Look for patterns like "product 123", "id 123", "#123"
        product_id_match = re.search(r'(?:product|id|#)\s*(\d+)', message, re.IGNORECASE)
        if product_id_match:
            product_id = int(product_id_match.group(1))
            product_details = self.tools.get_product_by_id(product_id)
            
            if "error" not in product_details:
                state.selected_product = product_details
        
        # Move to the order creation stage
        state.stage = "ordering"
        return {"stage": "ordering"}
    
    def _create_order(self, state: AgentState) -> Dict[str, Any]:
        # Check if we have a selected product and user intent to order
        message = state.chat_history[-1].content
        
        order_intent = any(keyword in message.lower() for keyword in 
                          ["order", "buy", "purchase", "checkout", "get this"])
        
        if state.selected_product and order_intent:
            # Try to extract quantity
            quantity_match = re.search(r'quantity\s*:?\s*(\d+)', message, re.IGNORECASE)
            quantity = int(quantity_match.group(1)) if quantity_match else 1
            
            # Try to extract size if applicable
            size_match = re.search(r'size\s*:?\s*(\w+)', message, re.IGNORECASE)
            size = size_match.group(1) if size_match else None
            
            # Extract user_id from the first message
            user_id = 1  # Default to 1 if not found
            
            # Create the order
            order_result = self.tools.create_order(
                user_id=user_id,
                product_id=state.selected_product["product_id"],
                quantity=quantity,
                size=size
            )
            
            state.order_details = order_result
        
        # Generate the final response
        state.stage = "generate_response"
        return {"stage": "generate_response"}
    
    def _generate_response(self, state: AgentState) -> Dict[str, Any]:
        # Generate a response based on the current state
        
        # Prepare the chat history for the LLM
        formatted_history = []
        for message in state.chat_history:
            if message.role == "user":
                formatted_history.append(HumanMessage(content=message.content))
            else:
                formatted_history.append(AIMessage(content=message.content))
        
        # Build context for response generation
        context = {
            "stage": state.stage,
            "search_results": state.search_results,
            "selected_product": state.selected_product,
            "order_details": state.order_details
        }
        
        # Generate a response using the LLM
        response = self.chain.invoke({
            "input": f"Given this state: {context}, generate a helpful response",
            "chat_history": formatted_history
        })
        
        # Add the response to the chat history
        state.chat_history.append(ChatMessage(role="assistant", content=response))
        
        return {"stage": END}
    
    def process_message(self, user_message: str, chat_history: List[Dict[str, str]], user_id: Optional[int] = None) -> Tuple[str, Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
        # Convert chat history to the format expected by the agent
        formatted_history = []
        for message in chat_history:
            formatted_history.append(ChatMessage(
                role=message["role"],
                content=message["content"]
            ))
        
        # Add the new user message
        formatted_history.append(ChatMessage(role="user", content=user_message))
        
        # Set the initial state
        initial_state = AgentState(
            chat_history=formatted_history,
            stage="initial"
        )
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        # Extract the response from the final state
        assistant_message = final_state.chat_history[-1].content
        
        return (
            assistant_message,
            final_state.search_results,
            final_state.order_details
        )