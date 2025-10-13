import os, json
import logging
import json
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
                # Parse parameters to avoid logging large datasets
                try:
                    params = json.loads(tool_call.function.arguments)
                    param_summary = {k: f"<{type(v).__name__}>" if isinstance(v, (list, dict)) and len(str(v)) > 100 else v
                                   for k, v in params.items()}
                    logger.info(f"Tool {i} Parameters: {param_summary}")
                except:
                    logger.info(f"Tool {i} Parameters: <unparseable>")
        else:
            logger.info("LLM made no tool calls")
        logger.info("=== END API ROUTER DECISION ===")

        # Check if LLM responded with clarifying questions instead of tool calls
        if not response.choices[0].message.tool_calls:
            clarification_response = response.choices[0].message.content
            if clarification_response:
                # Parse the consistent JSON response format
                try:
                    # Clean up the response and extract JSON
                    content = clarification_response.strip()

                    # Handle code blocks or plain JSON
                    if "```json" in content:
                        start = content.find("```json") + 7
                        end = content.find("```", start)
                        if end > start:
                            content = content[start:end].strip()
                    elif content.startswith('{') and content.endswith('}'):
                        # Already clean JSON
                        pass
                    else:
                        # Try to find JSON within the response
                        lines = content.split('\n')
                        for line in lines:
                            line = line.strip()
                            if line.startswith('{') and line.endswith('}'):
                                content = line
                                break

                    parsed_response = json.loads(content)

                    if isinstance(parsed_response, dict) and "type" in parsed_response:
                        response_type = parsed_response["type"]

                        if response_type == "api_call":
                            # Handle consistent API call format
                            function_name = parsed_response.get("function_name")
                            parameters = parsed_response.get("parameters", {})

                            logger.info(f"LLM provided consistent API call format: {function_name} with params {parameters}")

                            # Execute the API call
                            tool_result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")
                            return [{
                                "api_name": function_name,
                                "parameters": parameters,
                                "data": tool_result
                            }]

                        elif response_type == "clarification":
                            # Handle consistent clarification format
                            clarification_message = parsed_response.get("message", "")
                            logger.info("LLM provided consistent clarification format")
                            return [{"clarification": clarification_message}]

                    # Legacy fallback for old formats
                    elif isinstance(parsed_response, dict):
                        # Check for old tool call format like {"name":"functions.GetWorkOrderInformation","arguments":{}}
                        if "name" in parsed_response and "arguments" in parsed_response:
                            function_name = parsed_response["name"]
                            if function_name.startswith("functions."):
                                function_name = function_name[10:]

                            arguments = parsed_response["arguments"]
                            logger.info(f"LLM provided legacy tool call format: {function_name} with args {arguments}")

                            tool_result = execute_api("AITransmissionWorkOrder", function_name, arguments, auth_token, method="POST")
                            return [{
                                "api_name": function_name,
                                "parameters": arguments,
                                "data": tool_result
                            }]

                        # Legacy check for contractor parameters
                        elif any(key in parsed_response for key in ['ContractorName', 'ContractorCWIName', 'ContractorNDEName', 'ContractorCRIName']):
                            logger.info(f"LLM provided legacy parameters format: {parsed_response}")
                            tool_result = execute_api("AITransmissionWorkOrder", "GetWorkOrderInformation", parsed_response, auth_token, method="POST")
                            return [{
                                "api_name": "GetWorkOrderInformation",
                                "parameters": parsed_response,
                                "data": tool_result
                            }]

                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response: {e}")
                except Exception as e:
                    logger.warning(f"Error processing response format: {e}")

                # If no structured format found, treat as plain clarification
                logger.info("LLM provided plain text clarification")
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

def data_analysis_step(user_input, api_results, api_name=None, api_parameters=None):
    """
    Data analysis with raw API results - AI handles nested structures and counting.

    Args:
        user_input (str): User's query
        api_results (list): Raw API results with nested structures
        api_name (str): Name of the API that was called
        api_parameters (dict): Parameters used to filter the data

    Returns:
        str: AI analysis response
    """
    if api_parameters is None:
        api_parameters = {}

    logger.info(f"Starting data analysis with raw API results")

    # Get the analysis prompt with raw data
    analysis_prompt = get_data_analysis_prompt(user_input, api_results, api_name, api_parameters)

    messages = [
        {
            "role": "system",
            "content": analysis_prompt
        },
        {
            "role": "user",
            "content": f"Analyze the API data to answer: {user_input}"
        }
    ]

    try:
        response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=messages,
            temperature=0.1
        )
        ai_response = response.choices[0].message.content

        logger.info("Data analysis completed successfully")

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

        # Extract API name and parameters from first result
        api_name = api_results[0].get("api_name", "Unknown") if api_results else "Unknown"
        api_parameters = api_results[0].get("parameters", {}) if api_results else {}
        logger.info(f"Processing raw data for API: {api_name}")

        logger.info("Step 2: Data Analysis - Analyzing raw API data...")
        # Step 2: Pass raw API results to analysis agent
        final_response = data_analysis_step(user_input, api_results, api_name, api_parameters)

        return final_response

    except Exception as e:
        logger.error(f"WeldInsights processing failed: {str(e)}")
        return f"Error in WeldInsights two-step processing: {str(e)}"
