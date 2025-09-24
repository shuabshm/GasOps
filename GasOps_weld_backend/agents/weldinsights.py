import os, json
import logging
from config.azure_client import get_azure_chat_openai
from tools.execute_api import execute_api
from tools.weldinsights_tools import get_weldinsights_tools
from prompts.weld_api_router_prompt import get_api_router_prompt
from prompts.weld_analysis_prompt import get_data_analysis_prompt

logger = logging.getLogger(__name__)

# Initialize Azure OpenAI client
try:
    azure_client, azureopenai = get_azure_chat_openai()
    logger.info("Azure OpenAI client initialized for WeldInsights agent")
except Exception as e:
    logger.error(f"Failed to initialize Azure OpenAI client in WeldInsights agent: {str(e)}")
    azure_client, azureopenai = None, None

def execute_weldinsights_tool_call(tool_call, auth_token=None):
    """
    Execute the tool function using execute_api directly with function name as API name.

    Args:
        tool_call: OpenAI tool call object containing function name and arguments
        auth_token (str, optional): Authentication token for API calls

    Returns:
        dict: API response data
    """
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    api_path = arguments.pop("api_path", "AITransmissionWorkOrder")
    parameters = {k: v for k, v in arguments.items() if v is not None}

    logger.info(f"Executing WeldInsights tool: {function_name}")

    try:
        result = execute_api(api_path, function_name, parameters, auth_token, method="POST")
        logger.info(f"WeldInsights tool {function_name} executed successfully")
        return result
    except Exception as e:
        logger.error(f"WeldInsights tool {function_name} failed: {str(e)}")
        return {"error": f"Tool execution failed: {str(e)}"}

def extract_clean_data(api_results):
    """
    Extract only the actual data arrays from API responses.

    This function processes API responses and extracts the actual work order data,
    removing metadata and response structure wrapper.

    Args:
        api_results (list): List of API response objects

    Returns:
        list: Clean array of work order objects
    """
    clean_data_arrays = []
    
    for api_result in api_results:
        if "error" in api_result:
            continue
        
        # Navigate the actual API response structure
        api_data = api_result.get("data", {})
        
        # Based on debug output: api_result["data"]["data"]["Data"]
        data_array = None
        if isinstance(api_data, dict) and "data" in api_data:
            nested_data = api_data["data"]
            if isinstance(nested_data, dict) and "Data" in nested_data:
                data_array = nested_data["Data"]
                logger.info(f"Successfully extracted data array from {api_result.get('api_name', 'unknown')} API")
        
        # Process the data array
        if data_array is not None and isinstance(data_array, list):
            clean_data_arrays.extend(data_array)
            logger.info(f"Extracted {len(data_array)} work order objects from {api_result.get('api_name', 'unknown')} API")
        else:
            logger.warning(f"Could not extract data array from {api_result.get('api_name', 'unknown')} API - data_array is {type(data_array)}")
    
    logger.info(f"Total clean work order objects extracted: {len(clean_data_arrays)}")

    # Log cleaned data structure for debugging
    if len(clean_data_arrays) > 0:
        sample_ids = [wo.get('TransmissionWorkOrderID', 'N/A') for wo in clean_data_arrays[:5] if isinstance(wo, dict)]
        logger.info(f"Sample TransmissionWorkOrderIDs: {sample_ids}")
    
    return clean_data_arrays

def api_router_step(user_input, auth_token=None):
    """Step 1: API Router - Selects and calls appropriate APIs"""
    router_prompt = get_api_router_prompt(user_input)
    messages = [
        {
            "role": "system",
            "content": router_prompt
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    try:
        # API Router call with tools
        response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=messages,
            tools=get_weldinsights_tools(),
            tool_choice="auto",  # Allow LLM to ask clarifying questions when needed
            temperature=0.0  # Low temperature for precise API selection
        )

        # Log the LLM's API routing decision
        logger.info("=== API ROUTER LLM DECISION ===")

        # Log raw LLM response content if available
        response_content = response.choices[0].message.content
        if response_content:
            logger.info(f"LLM Response Content: {response_content}")

        # Log tool calls and parameters
        if response.choices[0].message.tool_calls:
            logger.info(f"LLM selected {len(response.choices[0].message.tool_calls)} tool(s) to call:")
            for i, tool_call in enumerate(response.choices[0].message.tool_calls, 1):
                logger.info(f"Tool {i}: {tool_call.function.name}")
                logger.info(f"Tool {i} Parameters: {tool_call.function.arguments}")
        else:
            logger.info("LLM made no tool calls")
        logger.info("=== END API ROUTER DECISION ===")

        # Check if LLM responded with clarifying questions instead of tool calls
        if not response.choices[0].message.tool_calls:
            clarification_response = response.choices[0].message.content
            if clarification_response:
                # Check if LLM provided JSON parameters instead of calling tool
                try:
                    # Handle multiple JSON objects in response - try to extract the first one
                    lines = clarification_response.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('{') and line.endswith('}'):
                            try:
                                parsed_params = json.loads(line)
                                if isinstance(parsed_params, dict) and any(key in parsed_params for key in ['ContractorName', 'ContractorCWIName', 'ContractorNDEName', 'ContractorCRIName']):
                                    logger.info(f"LLM provided parameters in JSON format: {parsed_params}")
                                    # Manually create a tool call result
                                    tool_result = execute_api("AITransmissionWorkOrder", "GetWorkOrderInformation", parsed_params, auth_token, method="POST")
                                    return [{
                                        "api_name": "GetWorkOrderInformation",
                                        "parameters": parsed_params,
                                        "data": tool_result
                                    }]
                            except json.JSONDecodeError:
                                continue
                except Exception as e:
                    logger.info(f"Error processing response format: {e}")

                # If not JSON parameters, treat as clarification question
                logger.info("LLM is asking for clarification - returning response to user")
                return [{"clarification": clarification_response}]
            else:
                logger.warning("LLM made no tool calls and provided no content")
                return [{"error": "No tools selected and no clarification provided"}]

        # Execute tool calls and collect data
        api_results = []
        for tool_call in response.choices[0].message.tool_calls:
            logger.info(f"Step 1 - Executing tool: {tool_call.function.name}")
            tool_result = execute_weldinsights_tool_call(tool_call, auth_token)
            api_results.append({
                "api_name": tool_call.function.name,
                "parameters": json.loads(tool_call.function.arguments),
                "data": tool_result
            })

        return api_results

    except Exception as e:
        logger.error(f"API Router error: {str(e)}")
        return [{"error": f"API Router error: {str(e)}"}]

def data_analysis_step(user_input, clean_data_array):
    """
    Enhanced data analysis with truncation detection.

    Args:
        user_input (str): User's query
        clean_data_array (list): Clean array of work order data

    Returns:
        str: AI analysis response
    """
    import json
    
    logger.info(f"Starting data analysis with {len(clean_data_array)} records")
    
    # Check for potential truncation issues
    try:
        data_json = json.dumps(clean_data_array)
        data_size = len(data_json)
        logger.info(f"Total data size: {data_size} characters")
        
        # Check if data might be too large for AI context
        if data_size > 200000:  # 200k characters
            logger.warning("Data size exceeds safe limits - truncation likely")
        elif data_size > 100000:  # 100k characters
            logger.warning("Data size is very large - potential truncation risk")
        else:
            logger.info("Data size is within safe limits")
            
        # Test if we can recreate the JSON properly
        reconstructed = json.loads(data_json)
        if len(reconstructed) != len(clean_data_array):
            logger.error(f"JSON reconstruction failed. Original: {len(clean_data_array)}, Reconstructed: {len(reconstructed)}")
        else:
            logger.info(f"JSON reconstruction successful - {len(reconstructed)} records")
            
    except Exception as e:
        logger.error(f"JSON processing failed: {str(e)}")
    
    # Show first and last few records to verify completeness
    if len(clean_data_array) > 0:
        first_id = clean_data_array[0].get('TransmissionWorkOrderID', 'N/A') if isinstance(clean_data_array[0], dict) else 'N/A'
        last_id = clean_data_array[-1].get('TransmissionWorkOrderID', 'N/A') if isinstance(clean_data_array[-1], dict) else 'N/A'
        sample_ids = [wo.get('TransmissionWorkOrderID', 'N/A') for wo in clean_data_array[:5] if isinstance(wo, dict)]
        logger.info(f"Data range - First ID: {first_id}, Last ID: {last_id}, Sample IDs: {sample_ids}")
    
    analysis_prompt = get_data_analysis_prompt(user_input, clean_data_array)
    
    # Check prompt size
    prompt_size = len(analysis_prompt)
    logger.info(f"Analysis prompt size: {prompt_size} characters")
    if prompt_size > 150000:
        logger.warning("Prompt size is very large - may cause AI processing issues")
    
    messages = [
        {
            "role": "system",
            "content": analysis_prompt
        },
        {
            "role": "user",
            "content": f"Analyze the complete dataset to answer: {user_input}"
        }
    ]

    try:
        response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=messages,
            temperature=0.0  # Zero temperature for precise data analysis and counting
        )
        ai_response = response.choices[0].message.content
        
        logger.info("Data analysis completed successfully")

        # Try to extract count from AI response for verification
        import re
        count_matches = re.findall(r'\b(\d+)\b', ai_response)
        if count_matches:
            logger.info(f"Numbers found in AI response: {count_matches}, Expected count: {len(clean_data_array)}")
        
        return ai_response

    except Exception as e:
        logger.error(f"AI processing failed: {str(e)}")
        return f"Data Analysis error: {str(e)}"

def handle_weldinsights(user_input, auth_token=None):
    """
    Main WeldInsights handler that processes user queries through API routing and data analysis.

    Args:
        user_input (str): User's query about work orders
        auth_token (str, optional): Authentication token for API calls

    Returns:
        str: Processed response from data analysis
    """
    try:
        logger.info("Step 1: API Router - Fetching data...")
        # Step 1: Get raw data from APIs
        api_results = api_router_step(user_input, auth_token)

        # Handle clarification requests from API router
        if api_results and len(api_results) == 1 and "clarification" in api_results[0]:
            return api_results[0]["clarification"]

        if not api_results or (len(api_results) == 1 and "error" in api_results[0]):
            return api_results[0].get("error", "No data retrieved from APIs")

        # Log API results structure for debugging
        logger.info(f"Received {len(api_results)} API results")
        for i, result in enumerate(api_results):
            if "data" in result and isinstance(result["data"], dict):
                nested_data = result["data"].get("data", {})
                if isinstance(nested_data, dict) and "Data" in nested_data:
                    data_obj = nested_data["Data"]
                    if data_obj is not None and isinstance(data_obj, (list, str)):
                        data_length = len(data_obj)
                        logger.info(f"API Result {i+1}: Contains {data_length} data objects")
                    else:
                        logger.info(f"API Result {i+1}: Data field is {type(data_obj)}")

        logger.info("Step 1.5: Extracting clean data arrays...")
        # NEW STEP: Extract only the actual work order objects
        clean_data_array = extract_clean_data(api_results)

        if not clean_data_array:
            logger.warning("No clean data extracted. No work orders found matching the criteria.")
            # Pass empty array to data analysis to handle "no data found" case properly
            final_response = data_analysis_step(user_input, [])
            return final_response

        logger.info("Step 2: Data Analysis - Analyzing clean data...")
        # Step 2: Analyze the clean data array
        final_response = data_analysis_step(user_input, clean_data_array)

        return final_response

    except Exception as e:
        logger.error(f"WeldInsights processing failed: {str(e)}")
        return f"Error in WeldInsights two-step processing: {str(e)}"
