from langchain.schema import HumanMessage, SystemMessage
from api_client import APIClient
import json
from azure_client import get_azure_chat_openai
from api_knowledge_base import API_KNOWLEDGE_BASE, get_agent_apis
import logging

logger = logging.getLogger(__name__)

class WeldInsightAgent:
    def __init__(self):
        try:
            self.azure_client = get_azure_chat_openai()
            logger.info("WeldInsight agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
            raise e
    
    async def process(self, query, auth_token):
        """Process weld queries using AI-only classification with comprehensive API knowledge"""
        try:
            logger.info(f"Processing WeldInsight query: {query}")
            
            # Create API client with auth token
            api_client = APIClient()
            api_client.auth_token = auth_token
            
            # Use AI with full API knowledge to classify and select appropriate API
            ai_result = self._ai_classify_with_full_context(query)
            logger.info(f"AI classification result: {ai_result}")
            
            # Call the selected API with extracted parameters
            api_result = await self._execute_selected_api(ai_result, api_client)
            
            return {
                "success": api_result.get("success", True),
                "data": api_result.get("data"),
                "error": api_result.get("error"),
                "ai_classification": ai_result,
                "agent": "weldInsight agent",
                "apis_called": api_result.get("apis_called", [])
            }
            
        except Exception as e:
            logger.error(f"WeldInsight agent processing failed: {str(e)}")
            return {
                "success": False, 
                "error": str(e), 
                "agent": "weldInsight agent", 
                "apis_called": []
            }
    
    def _ai_classify_with_full_context(self, query):
        """Use AI with complete API knowledge to classify and extract parameters"""
        
        # Get all weld APIs for context
        weld_apis = get_agent_apis("WeldInsight")
        api_context = self._build_comprehensive_api_context(weld_apis)
        
        prompt = f"""
You are an expert API selector for GasOps WeldInsight system with complete knowledge of all available APIs.

AVAILABLE WELD APIS:
{api_context}

USER QUERY: "{query}"

TASK:
1. Analyze the user's question to understand what they want
2. Select the most appropriate API from the available options
3. Extract all required parameters from the query
4. Identify any missing required parameters

RESPOND IN JSON:
{{
    "selected_api": "api_name_from_available_list",
    "reasoning": "detailed explanation of why this API was selected",
    "confidence": 0.95,
    "parameters": {{
        "wr_number": "extracted_value_or_empty_string",
        "weld_serial_number": "extracted_value_or_empty_string",
        "weld_id": "extracted_value_or_empty_string"
    }},
    "missing_required_params": ["list_of_missing_params"],
    "validation_passed": true
}}
"""
        
        try:
            response = self.azure_client.invoke(prompt)
            ai_response = response.content.strip()
            
            # Clean JSON response if needed
            if ai_response.startswith('```json'):
                ai_response = ai_response.strip('```json').strip('```').strip()
            
            result = json.loads(ai_response)
            return result
            
        except Exception as e:
            logger.error(f"AI classification failed: {str(e)}")
            # Production fallback - default to most common API
            return {
                "selected_api": "weld_details_by_work_order",
                "reasoning": "Fallback due to classification error",
                "confidence": 0.1,
                "parameters": {"wr_number": "", "weld_serial_number": "", "weld_id": ""},
                "missing_required_params": ["wr_number"],
                "validation_passed": False
            }
    
    async def _execute_selected_api(self, ai_result, api_client):
        """Execute the API selected by AI with proper parameter validation"""
        
        selected_api = ai_result.get("selected_api")
        parameters = ai_result.get("parameters", {})
        missing_params = ai_result.get("missing_required_params", [])
        
        # Validate that we have a selected API
        if not selected_api or selected_api not in API_KNOWLEDGE_BASE:
            return {
                "success": False,
                "error": f"Invalid or unknown API selected: {selected_api}",
                "apis_called": []
            }
        
        # Check for missing required parameters
        if missing_params:
            param_list = ", ".join(missing_params)
            return {
                "success": False,
                "error": f"Missing required parameters: {param_list}. Please provide these values.",
                "apis_called": []
            }
        
        # Get API configuration
        api_config = API_KNOWLEDGE_BASE[selected_api]
        logger.info(f"Executing API: {api_config['method']} with parameters: {parameters}")
        
        try:
            # Execute the appropriate API method dynamically
            method_name = api_config["method"]
            api_method = getattr(api_client, method_name)
            
            # Call API with appropriate parameters based on API type
            if selected_api in ["weld_details_by_work_order", "work_order_information"]:
                result = api_method(parameters.get("wr_number", ""))
                
            elif selected_api in [
                "weld_details_by_serial", "material_assets_by_weld", 
                "joiners_by_weld", "visual_inspection_results"
            ]:
                result = api_method(parameters.get("weld_serial_number", ""))
                
            elif selected_api in ["nde_cri_inspection", "nde_cri_tertiary_inspection"]:
                result = api_method(
                    parameters.get("wr_number", ""),
                    parameters.get("weld_id", "")
                )
            else:
                return {
                    "success": False,
                    "error": f"API method implementation not found: {method_name}",
                    "apis_called": [api_config["api_endpoint"]]
                }
            
            # Return standardized response
            return {
                "success": result.get("success", True) if isinstance(result, dict) else True,
                "data": result.get("data", result) if isinstance(result, dict) else result,
                "error": result.get("error") if isinstance(result, dict) else None,
                "api_used": selected_api,
                "apis_called": [api_config["api_endpoint"]]
            }
            
        except Exception as e:
            logger.error(f"API execution failed: {str(e)}")
            return {
                "success": False,
                "error": f"API call failed: {str(e)}",
                "apis_called": [api_config["api_endpoint"]]
            }
    
    def _build_comprehensive_api_context(self, weld_apis):
        """Build detailed API context for AI classification"""
        context = ""
        for api_name, config in weld_apis.items():
            context += f"""
API: {api_name}
Description: {config['description']}
Required Parameters: {config['required_params']}
Optional Parameters: {config['optional_params']}
Example Questions: {config['example_questions'][:2]}  # Show top 2 examples
Keywords/Triggers: {config['keywords'][:5]}  # Show top 5 keywords

"""
        return context
