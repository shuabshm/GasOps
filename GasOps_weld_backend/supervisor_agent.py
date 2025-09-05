from langchain.schema import HumanMessage, SystemMessage
import json
from azure_client import get_azure_chat_openai

class SupervisorAgent:
    def __init__(self):
        try:
            self.azure_client = get_azure_chat_openai()
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {str(e)}")
            raise e
    
    async def process(self, query, auth_token):
        try:
            # Step 1: Classify the query using AI
            classification = self._classify_query(query)
            print(f"Query classification: {classification}")
            
            # Step 2: Route to appropriate agent based on classification
            return await self._route_to_agent(classification, query, auth_token)
            
        except Exception as e:
            return {
                "success": False, 
                "error": f"Supervisor processing failed: {str(e)}", 
                "agent": "supervisor agent",
                "classification": "error"
            }
    
    def _classify_query(self, query):
        """Classify the user query using Azure OpenAI"""
        classification_prompt = f"""
You are a query classification system for a GasOps Weld management system. Analyze the user query and classify it into one of these three categories:

1. **general**: General questions, greetings, help requests, or queries not related to specific weld operations or property extraction
   - Examples: "Hi", "Hello", "How are you?", "What can you do?", "Help me", "Thank you"

2. **weldInsight agent**: Queries related to weld operations, work orders, welding details, MTR data, or industrial API calls
   - Examples: "Show me work order 12345", "Get weld details for WR123", "Find welds in project ABC", "MTR information for heat number XYZ"

3. **MTR agent**: Queries that require extracting specific properties, measurements, or technical specifications from documents or data
   - Examples: "Extract material properties", "Get pipe specifications", "What are the dimensions?", "Extract technical data"

Query to classify: "{query}"

Respond with ONLY a JSON object in this exact format:
{{
    "category": "general|weldInsight agent|MTR agent",
    "confidence": 0.95,
    "reasoning": "Brief explanation of why this category was chosen"
}}
"""
        
        try:
            messages = [
                SystemMessage(content="You are a precise query classifier. Respond only with valid JSON."),
                HumanMessage(content=classification_prompt)
            ]
            
            response = self.azure_client.invoke(messages)
            classification_text = response.content.strip()
            classification = json.loads(classification_text)
            
            # Validate the response
            valid_categories = ["general", "weldInsight agent", "MTR agent"]
            if classification.get("category") not in valid_categories:
                raise ValueError(f"Invalid category: {classification.get('category')}")
                
            return classification
            
        except Exception as e:
            print(f"Classification error: {str(e)}")
            # Default fallback classification
            return {
                "category": "general",
                "confidence": 0.5,
                "reasoning": f"Classification failed, defaulting to general: {str(e)}"
            }
    
    async def _route_to_agent(self, classification, query, auth_token):
        """Route the query to the appropriate agent based on classification"""
        category = classification.get("category", "general")
        
        if category == "general":
            # Handle general queries directly in supervisor using AI knowledge
            result = self._handle_general_query(query)
            
        elif category == "weldInsight agent":
            from weldInsight_agent import WeldInsightAgent
            agent = WeldInsightAgent()
            result = await agent.process(query, auth_token)
            
        elif category == "MTR agent":
            from mtr_agent import MTRAgent
            agent = MTRAgent()
            result = await agent.process(query, auth_token)
            
        else:
            # Fallback to handling as general query
            result = self._handle_general_query(query)
        
        # Add classification info to result
        if isinstance(result, dict):
            result["classification"] = classification
            result["supervisor agent"] = "handled_directly" if category == "general" else "routing_successful"
        
        return result
    
    def _handle_general_query(self, query):
        """Handle general queries directly in supervisor using AI knowledge"""
        try:
            system_prompt = """
You are a helpful assistant for the GasOps Weld Management System. You handle general inquiries, greetings, and provide information about the system's capabilities using your AI knowledge.

Key capabilities of the GasOps Weld System:
- Work Order Management: View and track welding work orders
- Weld Details: Access detailed information about specific welds
- MTR Data: Retrieve Material Test Reports and heat number information
- Project Tracking: Monitor welding projects and their progress
- Quality Assurance: Access inspection results and compliance data
- Property Extraction: Extract technical specifications and measurements

Guidelines:
- Be friendly and professional
- Keep responses concise but informative
- For technical welding questions, suggest using specific work order numbers or weld IDs
- For greetings, respond warmly and offer assistance
- If asked about system capabilities, provide the overview above
- Use your AI knowledge to answer general questions about welding, materials, or industrial processes
"""

            user_prompt = f"User query: {query}"
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.azure_client.invoke(messages)
            ai_response = response.content.strip()
            
            return {
                "success": True,
                "data": ai_response,
                "agent": "supervisor agent",
                "query_type": "general"
            }
            
        except Exception as e:
            # Fallback response patterns
            query_lower = query.lower()
            
            if any(greeting in query_lower for greeting in ["hi", "hello", "hey", "good morning", "good afternoon"]):
                fallback_response = "Hello! I'm your GasOps Weld Management assistant. I can help you with work orders, weld details, MTR data, property extraction, and general questions about welding and the system. How can I assist you today?"
            
            elif any(help_word in query_lower for help_word in ["help", "what can you do", "capabilities"]):
                fallback_response = """I can help you with:
• Work Order Management - View and track welding work orders
• Weld Details - Access specific weld information
• MTR Data - Retrieve Material Test Reports
• Property Extraction - Extract technical specifications
• General Questions - Answer questions about welding and the system

Try asking me something like "Show me work order 12345" or "What are the weld details for WR123"."""
            
            elif any(thanks in query_lower for thanks in ["thank", "thanks"]):
                fallback_response = "You're welcome! Feel free to ask if you need any more assistance with the GasOps Weld Management System."
            
            else:
                fallback_response = "I'm here to help with the GasOps Weld Management System. You can ask me about work orders, weld details, MTR data, property extraction, or general questions about welding. How can I assist you?"
            
            return {
                "success": True,
                "data": fallback_response,
                "agent": "supervisor agent", 
                "query_type": "general",
                "note": "fallback_response_used"
            }

