from azure_client import get_azure_chat_openai

azure_client = get_azure_chat_openai()

class SupervisorAgent:
    async def process(self, query, auth_token):
        try:
            # Classify and route the query
            classification = self._classify_query(query)
            print(f"Query classification: {classification}")
            
            return await self._route_to_agent(classification, query, auth_token)
            
        except Exception as e:
            return {
                "success": False, 
                "error": f"Supervisor processing failed: {str(e)}", 
                "agent": "supervisor agent",
                "apis_called": ["/supervisor"]
            }
    
    def _classify_query(self, query):
        """Classify the user query using Azure OpenAI"""
        prompt = f"""
You are an expert assistant for a GasOps Weld management system.

Instructions:
- If the user's question is a general question (greetings, what's the date, general engineering, design calculations, standards, formulas, or topics about pipe properties, MAOP, wall thickness, steel grade, ASME codes, etc.), answer it directly and concisely.
- If the question is about work orders, weld details, or industrial operations, return: WELD-INSIGHT
- If the question is about material properties or properties analysis, MTR documents, technical specifications, compliance, or extracting data from documents, return: MTR-AGENT

User Question: {query}

Answer or Routing intent:
"""
        
        try:
            response = azure_client.invoke(prompt)
            content = response.content.strip()
            
            # If LLM returns routing intent, treat as intent, else as direct answer
            if content in ["WELD-INSIGHT", "MTR-AGENT"]:
                return content
            return {"type": "direct_answer", "answer": content}
            
        except Exception as e:
            print(f"Classification error: {str(e)}")
            return {"type": "direct_answer", "answer": "Hello! I'm here to help with the GasOps Weld Management System. How can I assist you?"}
    
    async def _route_to_agent(self, classification, query, auth_token):
        """Route the query to the appropriate agent based on classification"""
        
        # Handle direct answers from classification
        if isinstance(classification, dict) and classification.get("type") == "direct_answer":
            return {
                "success": True,
                "data": classification["answer"],
                "agent": "supervisor agent",
                "apis_called": ["/supervisor"]
            }
        
        # Route to specific agents
        if classification == "WELD-INSIGHT":
            from weldInsight_agent import WeldInsightAgent
            agent = WeldInsightAgent()
            return await agent.process(query, auth_token)
            
        elif classification == "MTR-AGENT":
            from mtr_agent import MTRAgent
            agent = MTRAgent()
            return await agent.process(query, auth_token)
            
        else:
            # Fallback - treat as general query
            return {
                "success": True,
                "data": "I'm here to help with the GasOps Weld Management System. How can I assist you?",
                "agent": "supervisor agent",
                "apis_called": ["/supervisor"]
            }

