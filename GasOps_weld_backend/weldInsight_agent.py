from langchain.schema import HumanMessage, SystemMessage
from api_client import APIClient
import json
from azure_client import get_azure_chat_openai

class WeldInsightAgent:
    def __init__(self):
        try:
            self.azure_client = get_azure_chat_openai()
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {str(e)}")
            raise e
    
    async def process(self, query, auth_token):
        try:
            # Create API client with auth token (already processed)
            api_client = APIClient()
            
            # Use Azure AI to classify query
            ai_result = self._classify_query(query)
            
            # Call appropriate API
            api_result, apis_called = self._call_api(ai_result, api_client, auth_token)
            
            return {
                "success": api_result.get("success", False),
                "data": api_result.get("data"),
                "error": api_result.get("error"),
                "ai_classification": ai_result,
                "agent": "weldInsight agent",
                "apis_called": apis_called
            }
            
        except Exception as e:
            return {"success": False, "error": str(e), "agent": "weldInsight agent", "apis_called": ["/openai/chat/completions"]}
    
    def _classify_query(self, query):
        prompt = f"""
Analyze this query and respond with JSON only:

Query: "{query}"

Determine:
1. Type: "work_order", "weld", or "mtr" 
2. Extract parameters like WRNumber, ProjectNumber, etc.

JSON format:
{{
  "type": "work_order",
  "parameters": {{"wr_number": "123"}}
}}
"""
        
        try:
            messages = [
                SystemMessage(content="You are a query classifier. Respond only with JSON."),
                HumanMessage(content=prompt)
            ]
            
            response = self.azure_client.invoke(messages)
            ai_response = response.content.strip()
            return json.loads(ai_response)
            
        except Exception as e:
            # Simple fallback
            if "weld" in query.lower():
                return {"type": "weld", "parameters": {"wr_number": ""}}
            else:
                return {"type": "work_order", "parameters": {"wr_number": ""}}
    
    def _call_api(self, ai_result, api_client, auth_token):
        query_type = ai_result.get("type", "work_order")
        params = ai_result.get("parameters", {})
        apis_called = ["/openai/chat/completions"]  # Always includes OpenAI for classification
        
        # Set auth token for this API client instance
        api_client.auth_token = auth_token
        
        if query_type == "weld":
            wr_number = params.get("wr_number", "")
            if wr_number:
                apis_called.append("/api/WeldDetails/GetAllWeldDetailsByWorkOrder")
                return api_client.get_all_weld_details_by_work_order(wr_number), apis_called
            else:
                return {"success": False, "error": "WR Number required for weld queries"}, apis_called
        elif query_type == "mtr":
            company_mtr_file_id = params.get("company_mtr_file_id", "")
            heat_number = params.get("heat_number", "")
            if company_mtr_file_id and heat_number:
                apis_called.append("/api/AIMTRMetaData/GetMTRMetaData")
                return api_client.get_mtr_metadata(company_mtr_file_id, heat_number), apis_called
            else:
                return {"success": False, "error": "Company MTR File ID and Heat Number required for MTR queries"}, apis_called
        else:
            wr_number = params.get("wr_number", "")
            if wr_number:
                apis_called.append("/api/WorkOrder/GetWorkOrderInformation")
                return api_client.get_work_order_information(wr_number), apis_called
            else:
                return {"success": False, "error": "WR Number required for work order queries"}, apis_called
