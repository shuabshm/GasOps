from openai import AzureOpenAI
from api_client import APIClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseAgent:
    def __init__(self):
        self.azure_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        )
        self.api_client = APIClient()
    
    async def process(self, query, auth_token):
        try:
            # Use Azure AI to classify query
            ai_result = await self._classify_query(query)
            
            # Call appropriate API
            api_result = self._call_api(ai_result, auth_token)
            
            return {
                "success": api_result.get("success", False),
                "data": api_result.get("data"),
                "error": api_result.get("error"),
                "ai_classification": ai_result,
                "agent": "database_agent"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e), "agent": "database_agent"}
    
    async def _classify_query(self, query):
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
            response = await self.azure_client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4"),
                messages=[
                    {"role": "system", "content": "You are a query classifier. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            ai_response = response.choices[0].message.content.strip()
            return json.loads(ai_response)
            
        except Exception as e:
            # Simple fallback
            if "weld" in query.lower():
                return {"type": "weld", "parameters": {"wr_number": ""}}
            else:
                return {"type": "work_order", "parameters": {"wr_number": ""}}
    
    def _call_api(self, ai_result, auth_token):
        query_type = ai_result.get("type", "work_order")
        params = ai_result.get("parameters", {})
        
        if query_type == "weld":
            wr_number = params.get("wr_number", "")
            if wr_number:
                return self.api_client.get_all_weld_details_by_work_order(wr_number)
            else:
                return {"success": False, "error": "WR Number required for weld queries"}
        elif query_type == "mtr":
            company_mtr_file_id = params.get("company_mtr_file_id", "")
            heat_number = params.get("heat_number", "")
            if company_mtr_file_id and heat_number:
                return self.api_client.get_mtr_metadata(company_mtr_file_id, heat_number)
            else:
                return {"success": False, "error": "Company MTR File ID and Heat Number required for MTR queries"}
        else:
            wr_number = params.get("wr_number", "")
            if wr_number:
                return self.api_client.get_work_order_information(wr_number)
            else:
                return {"success": False, "error": "WR Number required for work order queries"}
