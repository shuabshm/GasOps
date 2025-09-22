# WeldInsight Agent - Welding Operations and Work Order Specialist
# Advanced AI agent for processing welding-related queries and work order management
# Handles weld details, inspections, material assets, and industrial operations data

import json
import logging
from config.azure_client import get_azure_chat_openai
from tools.calling_api_weld import call_weld_api
from tools.weldinsight_tools import get_weldinsight_tools
from prompts.weldinsight_data_collection_prompt import get_weldinsight_data_collection_prompt
from prompts.weldinsight_analysis_prompt import get_weldinsight_analysis_prompt

logger = logging.getLogger(__name__)

# Initialize Azure OpenAI client for intelligent query processing
azure_client, azureopenai = get_azure_chat_openai()

def execute_tool_call(tool_call, auth_token=None):
    """
    Execute tool function calls for welding operations.

    Maps OpenAI function calls to appropriate welding API tool functions,
    handling parameter transformation and authentication.

    Args:
        tool_call: OpenAI tool call object with function name and arguments
        auth_token (str): Authentication token for external API calls

    Returns:
        dict: API response with success status and welding data
    """
    from tools.weldinsight_tools import (
        GetAllWeldDetailsByWorkOrder,
        GetWorkOrderInformationAndAssignment,
        GetWeldDetailsByWeldSerialNumber,
        GetMaterialAssetsByWeldSerialNumber,
        GetJoinersByWeldSerialNumber,
        GetVisualInspectionResultsByWeldSerialNumber,
        GetNDEAndCRIInspectionDetails,
        GetNDECRIAndTertiaryInspectionDetails
    )

    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # Add auth_token to arguments
    arguments['auth_token'] = auth_token

    # Map function names to actual tool functions
    tool_functions = {
        'GetAllWeldDetailsByWorkOrder': GetAllWeldDetailsByWorkOrder,
        'GetWorkOrderInformationAndAssignment': GetWorkOrderInformationAndAssignment,
        'GetWeldDetailsByWeldSerialNumber': GetWeldDetailsByWeldSerialNumber,
        'GetMaterialAssetsByWeldSerialNumber': GetMaterialAssetsByWeldSerialNumber,
        'GetJoinersByWeldSerialNumber': GetJoinersByWeldSerialNumber,
        'GetVisualInspectionResultsByWeldSerialNumber': GetVisualInspectionResultsByWeldSerialNumber,
        'GetNDEAndCRIInspectionDetails': GetNDEAndCRIInspectionDetails,
        'GetNDECRIAndTertiaryInspectionDetails': GetNDECRIAndTertiaryInspectionDetails
    }

    # Execute the appropriate tool function
    if function_name in tool_functions:
        return tool_functions[function_name](**arguments)
    else:
        return {"error": f"Unknown function: {function_name}"}

def handle_weldinsight_agent(user_input, auth_token=None):
    """
    Main WeldInsight agent handler for processing welding and work order queries.

    This function manages the complete welding operations workflow using a two-step AI approach:
    1. Step 1 AI: Analyzes user queries to identify welding-related intent and selects appropriate API tools
    2. Executes API calls with proper authentication and parameter handling
    3. Step 2 AI: Analyzes collected data with strict accuracy requirements to prevent hallucination
    4. Formats responses for comprehensive welding operation insights

    Args:
        user_input (str): User's query about welding operations or work orders
        auth_token (str, optional): Authentication token for API calls

    Returns:
        dict: Structured response with success status, data, and agent identification

    Supported Operations:
    - Work order information and assignments
    - Weld details by serial number or work order
    - Material assets tracking
    - Joiner information and qualifications
    - Visual and NDE inspection results
    - CRI and tertiary inspection data
    """

    logger.info(f"=== WELDINSIGHT AGENT STARTED (TWO-STEP APPROACH) ===")
    logger.info(f"User input: {user_input}")
    logger.info(f"Auth token available: {bool(auth_token)}")

    try:
        # STEP 1: Data Collection AI - Tool Selection and Parameter Extraction
        logger.info(f"=== STEP 1: DATA COLLECTION AI ===")
        logger.info(f"=== GENERATING DATA COLLECTION PROMPT ===")
        data_collection_prompt = get_weldinsight_data_collection_prompt(user_input)
        logger.info(f"Data collection prompt generated - length: {len(data_collection_prompt)} characters")

        # Create messages list for Step 1 AI
        step1_messages = [
            {
                "role": "system",
                "content": data_collection_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
        logger.info(f"Created Step 1 conversation messages - count: {len(step1_messages)}")

        # Step 1 AI call with function calling for intelligent tool selection
        logger.info(f"=== CALLING AZURE OPENAI FOR TOOL SELECTION (STEP 1) ===")
        logger.info(f"Model: {azureopenai}")
        logger.info(f"Tools available: {len(get_weldinsight_tools())}")

        step1_response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=step1_messages,
            tools=get_weldinsight_tools(),
            tool_choice="required",  # Forces the LLM to call at least one tool
            temperature=0.1  # Maximum accuracy and determinism for data analysis
        )

        logger.info(f"=== STEP 1 AZURE OPENAI TOOL SELECTION RESPONSE ===")
        logger.info(f"Response has tool calls: {bool(step1_response.choices[0].message.tool_calls)}")

        # Collect all tool results
        all_tool_results = []

        # Check if the model wants to call a tool
        if step1_response.choices[0].message.tool_calls:
            tool_calls = step1_response.choices[0].message.tool_calls
            logger.info(f"Number of tool calls: {len(tool_calls)}")

            # Execute each tool call and collect results
            for i, tool_call in enumerate(tool_calls):
                logger.info(f"=== EXECUTING TOOL CALL {i+1}/{len(tool_calls)} ===")
                logger.info(f"Tool: {tool_call.function.name}")
                logger.info(f"Arguments: {tool_call.function.arguments}")

                # Execute the tool function
                tool_result = execute_tool_call(tool_call, auth_token)
                logger.info(f"=== TOOL EXECUTION RESULT ===")
                logger.info(f"Tool result type: {type(tool_result)}")
                logger.info(f"Tool result success: {tool_result.get('success', 'No success field') if isinstance(tool_result, dict) else 'Not a dict'}")
                if isinstance(tool_result, dict):
                    logger.info(f"Tool result keys: {list(tool_result.keys())}")
                    if 'data' in tool_result:
                        data = tool_result['data']
                        logger.info(f"Data type: {type(data)}")
                        if isinstance(data, dict) and 'Obj' in data:
                            logger.info(f"API response has 'Obj' field with {len(data['Obj']) if data['Obj'] else 0} items")
                        elif isinstance(data, list):
                            logger.info(f"Data is list with {len(data)} items")
                        elif isinstance(data, dict) and 'Data' in data:
                            actual_data_array = data['Data']
                            logger.info(f"CRITICAL: API response 'Data' field contains {len(actual_data_array)} weld records")
                            logger.info(f"Data array type: {type(actual_data_array)}")
                        else:
                            logger.info(f"Data content preview: {str(data)[:200]}...")

                # Store tool result for Step 2
                all_tool_results.append({
                    "tool_name": tool_call.function.name,
                    "tool_arguments": tool_call.function.arguments,
                    "tool_result": tool_result
                })
                logger.info(f"Stored tool result for Step 2 analysis")

            # STEP 2: Analysis AI - Pure Data Analysis with Strict Counting Rules
            logger.info(f"=== STEP 2: ANALYSIS AI ===")
            logger.info(f"=== GENERATING ANALYSIS PROMPT ===")
            analysis_prompt = get_weldinsight_analysis_prompt(user_input)
            logger.info(f"Analysis prompt generated - length: {len(analysis_prompt)} characters")

            # Prepare data for Step 2 AI with enhanced debugging
            collected_data_summary = {
                "user_query": user_input,
                "tool_results": all_tool_results,
                "total_api_calls": len(all_tool_results)
            }

            # CRITICAL: Add explicit count verification for debugging
            for i, tool_result in enumerate(all_tool_results):
                if isinstance(tool_result.get('tool_result', {}).get('data'), dict):
                    api_data = tool_result['tool_result']['data']
                    if 'Data' in api_data and isinstance(api_data['Data'], list):
                        actual_count = len(api_data['Data'])
                        logger.info(f"VERIFICATION - Tool {i+1}: API Data array contains EXACTLY {actual_count} records")
                        # Add explicit count to the summary for Step 2 AI
                        tool_result['VERIFIED_RECORD_COUNT'] = actual_count
                        tool_result['COUNTING_INSTRUCTION'] = f"CRITICAL: This tool returned EXACTLY {actual_count} records in the Data array. Do not count any other fields."

            # Create messages for Step 2 AI
            step2_messages = [
                {
                    "role": "system",
                    "content": analysis_prompt
                },
                {
                    "role": "user",
                    "content": f"USER QUERY: {user_input}\n\nCOLLECTED API DATA: {json.dumps(collected_data_summary, indent=2)}"
                }
            ]
            logger.info(f"Created Step 2 conversation messages - count: {len(step2_messages)}")

            # Step 2 AI call for pure data analysis
            logger.info(f"=== CALLING AZURE OPENAI FOR DATA ANALYSIS (STEP 2) ===")
            logger.info(f"Model: {azureopenai}")
            logger.info(f"No tools needed - pure analysis")

            step2_response = azure_client.chat.completions.create(
                model=azureopenai,
                messages=step2_messages,
                temperature=0.0  # Maximum accuracy and determinism for data analysis
            )

            final_content = step2_response.choices[0].message.content
            logger.info(f"=== FINAL AI RESPONSE (STEP 2) ===")
            logger.info(f"Final response length: {len(final_content)} characters")
            logger.info(f"Final response preview: {final_content[:300]}...")

            return {
                "success": True,
                "data": final_content,
                "agent": "WeldInsight Agent"
            }
        else:
            # No tool calls needed, return direct response
            logger.info(f"=== NO TOOL CALLS REQUIRED ===")
            direct_response = step1_response.choices[0].message.content
            logger.info(f"Direct response: {direct_response}")
            return {
                "success": True,
                "data": direct_response,
                "agent": "WeldInsight Agent"
            }

    except Exception as e:
        logger.error(f"Error in WeldInsight agent processing: {str(e)}")
        return {
            "success": False,
            "error": f"Error in WeldInsight processing: {str(e)}",
            "agent": "WeldInsight Agent"
        }