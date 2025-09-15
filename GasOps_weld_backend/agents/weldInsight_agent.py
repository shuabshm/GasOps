# WeldInsight Agent - Welding Operations and Work Order Specialist
# Advanced AI agent for processing welding-related queries and work order management
# Handles weld details, inspections, material assets, and industrial operations data

import json
import logging
from config.azure_client import get_azure_chat_openai
from tools.calling_api_weld import call_weld_api
from tools.weldinsight_tools import get_weldinsight_tools
from prompts.weldinsight_prompt import get_weldinsight_prompt

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
    
    This function manages the complete welding operations workflow:
    1. Analyzes user queries to identify welding-related intent
    2. Selects appropriate API tools for work orders, weld details, or inspections
    3. Executes API calls with proper authentication and parameter handling
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
    
    # Get WeldInsight prompt
    weldinsight_prompt = get_weldinsight_prompt(user_input)
    
    # Create messages list for conversation
    messages = [
        {
            "role": "system",
            "content": weldinsight_prompt
        },
        {
            "role": "user", 
            "content": user_input
        }
    ]

    try:
        # Initial AI call with function calling for intelligent tool selection
        response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=messages,
            tools=get_weldinsight_tools(),
            tool_choice="required"  # Forces the LLM to call at least one tool
        )

        # Check if the model wants to call a tool
        if response.choices[0].message.tool_calls:
            # Add the assistant's response to messages
            messages.append(response.choices[0].message)
            
            # Execute each tool call
            for tool_call in response.choices[0].message.tool_calls:
                logger.info(f"Executing tool: {tool_call.function.name} with arguments: {tool_call.function.arguments}")
                
                # Execute the tool function
                tool_result = execute_tool_call(tool_call, auth_token)
                logger.info(f"Tool result success: {tool_result.get('success', False)}")
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result) if isinstance(tool_result, (dict, list)) else str(tool_result)
                })
            
            # Get final response from the model - it will format the results naturally
            final_response = azure_client.chat.completions.create(
                model=azureopenai,
                messages=messages
            )
            
            return {
                "success": True,
                "data": final_response.choices[0].message.content,
                "agent": "WeldInsight Agent"
            }
        else:
            # No tool calls needed, return direct response
            return {
                "success": True,
                "data": response.choices[0].message.content,
                "agent": "WeldInsight Agent"
            }

    except Exception as e:
        logger.error(f"Error in WeldInsight agent processing: {str(e)}")
        return {
            "success": False,
            "error": f"Error in WeldInsight processing: {str(e)}",
            "agent": "WeldInsight Agent"
        }