# import json
# import openai
# from sqlalchemy.orm import Session
# from user_management.models import Product, Order, OrderItem
# import dotenv
# import os



# # Ensure you have installed langgraph via pip
# dotenv.load_dotenv()

# # Configure your Azure OpenAI key (or normal OpenAI key if you’re using that)
# openai.api_key = os.getenv("OPENAI_API_KEY")


# # @node()
# def intent_extraction(user_message: str) -> dict:
#     """
#     This node sends the user message to Azure OpenAI (GPT-4) to extract intent.
#     The output should be a JSON object:
#       For search: { "action": "search", "query": "<search_query>" }
#       For order:  { "action": "order", "product_id": <id>, "quantity": <quantity> }
#     """
#     prompt = (
#         f"You are an assistant for an e-commerce platform. Analyze the following user message and determine the user's intent.\n\n"
#         f'User message: "{user_message}"\n\n'
#         "If the message is for a product search, return a JSON object with the following format:\n"
#         '{ "action": "search", "query": "<search_query>" }\n\n'
#         "If the message is to place an order, return a JSON object with the following format:\n"
#         '{ "action": "order", "product_id": <id>, "quantity": <quantity> }\n\n'
#         "Ensure your output is valid JSON."
#     )

#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are an assistant that extracts user intent for an e-commerce platform.",
#             },
#             {"role": "user", "content": prompt},
#         ],
#         max_tokens=150,
#     )

#     try:
#         result = json.loads(response["choices"][0]["message"]["content"])
#         return result
#     except Exception as e:
#         # Return an error structure if parsing fails.
#         return {"error": "Intent extraction failed"}


# # @node()
# def product_search(query: str, db: Session) -> str:
#     """
#     This node queries the product table based on the search query.
#     """
#     products = db.query(Product).filter(Product.product_name.ilike(f"%{query}%")).all()
#     if not products:
#         return "Sorry, no matching products found."

#     response_text = "Here are some products matching your search:\n"
#     for product in products:
#         response_text += (
#             f"- {product.product_name} (${product.price}) [ID: {product.product_id}]\n"
#         )
#     response_text += "\nPlease provide the product ID and quantity to place an order."
#     return response_text


# # @node()
# def order_placement(product_id: int, quantity: int, db: Session) -> str:
#     """
#     This node places an order for the provided product_id and quantity.
#     """
#     product = db.query(Product).filter(Product.product_id == product_id).first()
#     if not product:
#         return "Invalid product ID. Please try again."

#     # Create a new order (user_id is hardcoded for now; adapt as needed)
#     new_order = Order(user_id=1, status="Pending")
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)

#     # Add an order item to the order
#     order_item = OrderItem(
#         order_id=new_order.order_id, product_id=product_id, quantity=quantity
#     )
#     db.add(order_item)
#     db.commit()

#     return f"Order placed for {product.product_name}! Order ID: {new_order.order_id}."


# # @node()
# def decision(intent: dict, db: Session) -> str:
#     """
#     This node routes the intent to the appropriate function.
#     """
#     # Check if intent extraction resulted in an error.
#     if "error" in intent:
#         return "I couldn't extract the intent from your request. Please try again."

#     action = intent.get("action", "").lower()
#     if action == "search":
#         search_query = intent.get("query", "")
#         return product_search(search_query, db)
#     elif action == "order":
#         product_id = intent.get("product_id")
#         quantity = intent.get("quantity", 1)
#         if product_id is None:
#             return "I couldn't extract a valid product ID for your order. Please rephrase your order details."
#         return order_placement(product_id, quantity, db)
#     else:
#         return "I couldn't understand your request. Could you please rephrase?"


# def build_graph(db: Session) -> graph:
#     """
#     Build and return a LangGraph instance that wires the intent extraction and decision nodes.
#     """
#     graph1 = graph()
#     # Add our nodes with a name so we can call them later.
#     graph1.add_node(intent_extraction, name="intent_extraction")
#     graph1.add_node(product_search, name="product_search")
#     graph1.add_node(order_placement, name="order_placement")
#     graph1.add_node(decision, name="decision")

#     # Connect the intent extraction node's output to the decision node.
#     graph1.connect("intent_extraction", "decision", output="intent", input="intent")

#     # We don't connect product_search and order_placement directly because they are called within decision.
#     return graph1


# def process_ai_request_with_langgraph(user_message: str, db: Session) -> str:
#     """
#     Process the user message through the LangGraph and return the final response text.
#     """
#     graph1 = build_graph(db)
#     # Run the intent extraction node first.
#     intent = graph1.run_node("intent_extraction", user_message)
#     # Then pass the extracted intent to the decision node.
#     response_text = graph1.run_node("decision", intent, db)
#     return response_text
