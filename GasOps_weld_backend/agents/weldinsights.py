# import os, json
# import logging
# import json
# from config.azure_client import get_azure_chat_openai
# from tools.execute_api import execute_api
# from tools.weldinsights_tools import get_weldinsights_tools
# from prompts.weld_api_router_prompt import get_api_router_prompt
# from prompts.weld_analysis_prompt import get_data_analysis_prompt

# logger = logging.getLogger(__name__)

# # Initialize Azure OpenAI client
# try:
#     azure_client, azureopenai = get_azure_chat_openai()
#     logger.info("Azure OpenAI client initialized for WeldInsights agent")
# except Exception as e:
#     logger.error(f"Failed to initialize Azure OpenAI client in WeldInsights agent: {str(e)}")
#     azure_client, azureopenai = None, None

# def execute_weldinsights_tool_call(tool_call, auth_token=None):
#     """
#     Execute the tool function using execute_api directly with function name as API name.

#     Args:
#         tool_call: OpenAI tool call object containing function name and arguments
#         auth_token (str, optional): Authentication token for API calls

#     Returns:
#         dict: API response data
#     """
#     function_name = tool_call.function.name
#     arguments = json.loads(tool_call.function.arguments)
#     api_path = arguments.pop("api_path", "AITransmissionWorkOrder")
#     parameters = {k: v for k, v in arguments.items() if v is not None}

#     logger.info(f"Executing WeldInsights tool: {function_name}")

#     try:
#         result = execute_api(api_path, function_name, parameters, auth_token, method="POST")
#         logger.info(f"WeldInsights tool {function_name} executed successfully")
#         return result
#     except Exception as e:
#         logger.error(f"WeldInsights tool {function_name} failed: {str(e)}")
#         return {"error": f"Tool execution failed: {str(e)}"}

# def execute_multi_api_calls(calls, auth_token=None):
#     """
#     Execute multiple API calls to the same API with different parameters.
#     NEW modular function for multi-call feature.

#     Args:
#         calls (list): List of call objects, each containing function_name and parameters
#         auth_token (str, optional): Authentication token for API calls

#     Returns:
#         list: List of API result objects from all calls
#     """
#     api_results = []
#     warnings = []

#     for i, call in enumerate(calls, 1):
#         function_name = call.get("function_name")
#         parameters = call.get("parameters", {})

#         logger.info(f"Multi-call {i}/{len(calls)}: Executing {function_name} with parameters {parameters}")

#         try:
#             result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")
#             api_results.append({
#                 "api_name": function_name,
#                 "parameters": parameters,
#                 "data": result
#             })
#             logger.info(f"Multi-call {i}/{len(calls)}: Success")
#         except Exception as e:
#             logger.error(f"Multi-call {i}/{len(calls)}: Failed - {str(e)}")
#             warnings.append(f"Call {i} failed: {str(e)}")
#             # Continue with partial results

#     # Add warnings to results if any failures occurred
#     if warnings:
#         logger.warning(f"Multi-call completed with {len(warnings)} failures: {warnings}")

#     return api_results

# def deduplicate_data_by_json(clean_data_array):
#     """
#     Deduplicate records using JSON stringify approach.
#     NEW modular function for multi-call feature.

#     Args:
#         clean_data_array (list): List of data objects that may contain duplicates

#     Returns:
#         list: Deduplicated list of data objects
#     """
#     if not clean_data_array:
#         return clean_data_array

#     seen_json_keys = set()
#     deduplicated = []

#     for item in clean_data_array:
#         if isinstance(item, dict):
#             # Sort keys to ensure consistent JSON string regardless of field order
#             json_key = json.dumps(item, sort_keys=True)

#             if json_key not in seen_json_keys:
#                 seen_json_keys.add(json_key)
#                 deduplicated.append(item)
#         else:
#             # Not a dict, include anyway
#             deduplicated.append(item)

#     duplicates_removed = len(clean_data_array) - len(deduplicated)
#     if duplicates_removed > 0:
#         logger.info(f"Deduplication: Removed {duplicates_removed} duplicate records using JSON stringify")

#     return deduplicated

# def extract_clean_data(api_results):
#     """
#     Extract only the actual data from API responses.

#     Handles two patterns:
#     1. Array-based APIs (GetWorkOrderInformation, etc.): Returns list of objects
#     2. Nested object APIs (GetDetailsbyWeldSerialNumber): Returns single nested object

#     Args:
#         api_results (list): List of API response objects

#     Returns:
#         list: Clean data (list of objects OR single nested object wrapped in list)
#     """
#     clean_data_arrays = []

#     for api_result in api_results:
#         if "error" in api_result:
#             continue

#         api_name = api_result.get("api_name", "Unknown")

#         # Navigate the actual API response structure
#         api_data = api_result.get("data", {})

#         # Based on debug output: api_result["data"]["data"]["Data"]
#         data_array = None
#         if isinstance(api_data, dict) and "data" in api_data:
#             nested_data = api_data["data"]
#             if isinstance(nested_data, dict) and "Data" in nested_data:
#                 data_array = nested_data["Data"]
#                 logger.info(f"Successfully extracted Data field from {api_name} API")

#         # SPECIAL HANDLING FOR GetDetailsbyWeldSerialNumber
#         # This API returns nested object structure, not array
#         if api_name == "GetDetailsbyWeldSerialNumber":
#             if isinstance(data_array, dict):
#                 # It's a nested object with sections like "Overall Details", "Asset Details", etc.
#                 # Wrap it in a list so it can be processed uniformly
#                 clean_data_arrays.append(data_array)
#                 logger.info(f"Extracted nested object structure from {api_name} API (1 weld serial number)")
#             else:
#                 logger.warning(f"Unexpected data structure for {api_name} - expected dict, got {type(data_array)}")

#         # NORMAL HANDLING FOR ALL OTHER APIs
#         # These return arrays of objects
#         elif data_array is not None and isinstance(data_array, list):
#             clean_data_arrays.extend(data_array)
#             logger.info(f"Extracted {len(data_array)} work order objects from {api_name} API")
#         else:
#             logger.warning(f"Could not extract data array from {api_name} API - data_array is {type(data_array)}")

#     logger.info(f"Total clean data objects extracted: {len(clean_data_arrays)}")

#     # Log cleaned data structure for debugging
#     if len(clean_data_arrays) > 0:
#         first_item = clean_data_arrays[0]
#         if isinstance(first_item, dict):
#             # Check if it's a nested object (GetDetailsbyWeldSerialNumber) or regular object
#             if any(key in first_item for key in ["Overall Details", "Asset Details", "CWI and NDE Result Details"]):
#                 logger.info(f"First item is nested object with sections: {list(first_item.keys())}")
#             else:
#                 sample_ids = [wo.get('TransmissionWorkOrderID', 'N/A') for wo in clean_data_arrays[:5] if isinstance(wo, dict)]
#                 logger.info(f"Sample TransmissionWorkOrderIDs: {sample_ids}")

#     return clean_data_arrays

# def api_router_step(user_input, auth_token=None):
#     """Step 1: API Router - Selects and calls appropriate APIs"""
#     router_prompt = get_api_router_prompt(user_input)
#     messages = [
#         {
#             "role": "system",
#             "content": router_prompt
#         },
#         {
#             "role": "user",
#             "content": user_input
#         }
#     ]

#     try:
#         # API Router call with tools
#         response = azure_client.chat.completions.create(
#             model=azureopenai,
#             messages=messages,
#             tools=get_weldinsights_tools(),
#             tool_choice="auto",  # Allow LLM to ask clarifying questions when needed
#             temperature=0.0  # Low temperature for precise API selection
#         )

#         # Log the LLM's API routing decision
#         logger.info("=== API ROUTER LLM DECISION ===")

#         # Log raw LLM response content if available
#         response_content = response.choices[0].message.content
#         if response_content:
#             logger.info(f"LLM Response Content: {response_content}")

#         # Log tool calls and parameters
#         if response.choices[0].message.tool_calls:
#             logger.info(f"LLM selected {len(response.choices[0].message.tool_calls)} tool(s) to call:")
#             for i, tool_call in enumerate(response.choices[0].message.tool_calls, 1):
#                 logger.info(f"Tool {i}: {tool_call.function.name}")
#                 # Parse parameters to avoid logging large datasets
#                 try:
#                     params = json.loads(tool_call.function.arguments)
#                     param_summary = {k: f"<{type(v).__name__}>" if isinstance(v, (list, dict)) and len(str(v)) > 100 else v
#                                    for k, v in params.items()}
#                     logger.info(f"Tool {i} Parameters: {param_summary}")
#                 except:
#                     logger.info(f"Tool {i} Parameters: <unparseable>")
#         else:
#             logger.info("LLM made no tool calls")
#         logger.info("=== END API ROUTER DECISION ===")

#         # Check if LLM responded with clarifying questions instead of tool calls
#         if not response.choices[0].message.tool_calls:
#             clarification_response = response.choices[0].message.content
#             if clarification_response:
#                 # Parse the consistent JSON response format
#                 try:
#                     # Clean up the response and extract JSON
#                     content = clarification_response.strip()

#                     # Handle code blocks or plain JSON
#                     if "```json" in content:
#                         start = content.find("```json") + 7
#                         end = content.find("```", start)
#                         if end > start:
#                             content = content[start:end].strip()
#                     elif content.startswith('{') and content.endswith('}'):
#                         # Already clean JSON
#                         pass
#                     else:
#                         # Try to find JSON within the response
#                         lines = content.split('\n')
#                         for line in lines:
#                             line = line.strip()
#                             if line.startswith('{') and line.endswith('}'):
#                                 content = line
#                                 break

#                     parsed_response = json.loads(content)

#                     if isinstance(parsed_response, dict) and "type" in parsed_response:
#                         response_type = parsed_response["type"]

#                         if response_type == "api_call":
#                             # Check if this is multi-call format (has "calls" array)
#                             if "calls" in parsed_response and isinstance(parsed_response["calls"], list):
#                                 # MULTI-CALL FORMAT - NEW feature
#                                 calls = parsed_response["calls"]
#                                 logger.info(f"LLM provided multi-call format with {len(calls)} calls")

#                                 # Execute all calls using the new multi-call function
#                                 api_results = execute_multi_api_calls(calls, auth_token)
#                                 return api_results

#                             else:
#                                 # SINGLE-CALL FORMAT - Existing behavior (unchanged)
#                                 function_name = parsed_response.get("function_name")
#                                 parameters = parsed_response.get("parameters", {})

#                                 logger.info(f"LLM provided consistent API call format: {function_name} with params {parameters}")

#                                 # Execute the API call
#                                 tool_result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")
#                                 return [{
#                                     "api_name": function_name,
#                                     "parameters": parameters,
#                                     "data": tool_result
#                                 }]

#                         elif response_type == "clarification":
#                             # Handle consistent clarification format
#                             clarification_message = parsed_response.get("message", "")
#                             logger.info("LLM provided consistent clarification format")
#                             return [{"clarification": clarification_message}]

#                     # Legacy fallback for old formats
#                     elif isinstance(parsed_response, dict):
#                         # Check for old tool call format like {"name":"functions.GetWorkOrderInformation","arguments":{}}
#                         if "name" in parsed_response and "arguments" in parsed_response:
#                             function_name = parsed_response["name"]
#                             if function_name.startswith("functions."):
#                                 function_name = function_name[10:]

#                             arguments = parsed_response["arguments"]
#                             logger.info(f"LLM provided legacy tool call format: {function_name} with args {arguments}")

#                             tool_result = execute_api("AITransmissionWorkOrder", function_name, arguments, auth_token, method="POST")
#                             return [{
#                                 "api_name": function_name,
#                                 "parameters": arguments,
#                                 "data": tool_result
#                             }]

#                         # Legacy check for contractor parameters
#                         elif any(key in parsed_response for key in ['ContractorName', 'ContractorCWIName', 'ContractorNDEName', 'ContractorCRIName']):
#                             logger.info(f"LLM provided legacy parameters format: {parsed_response}")
#                             tool_result = execute_api("AITransmissionWorkOrder", "GetWorkOrderInformation", parsed_response, auth_token, method="POST")
#                             return [{
#                                 "api_name": "GetWorkOrderInformation",
#                                 "parameters": parsed_response,
#                                 "data": tool_result
#                             }]

#                 except json.JSONDecodeError as e:
#                     logger.warning(f"Failed to parse JSON response: {e}")
#                 except Exception as e:
#                     logger.warning(f"Error processing response format: {e}")

#                 # If no structured format found, treat as plain clarification
#                 logger.info("LLM provided plain text clarification")
#                 return [{"clarification": clarification_response}]
#             else:
#                 logger.warning("LLM made no tool calls and provided no content")
#                 return [{"error": "No tools selected and no clarification provided"}]

#         # Execute tool calls and collect data
#         api_results = []
#         for tool_call in response.choices[0].message.tool_calls:
#             logger.info(f"Step 1 - Executing tool: {tool_call.function.name}")
#             tool_result = execute_weldinsights_tool_call(tool_call, auth_token)
#             api_results.append({
#                 "api_name": tool_call.function.name,
#                 "parameters": json.loads(tool_call.function.arguments),
#                 "data": tool_result
#             })

#         return api_results

#     except Exception as e:
#         logger.error(f"API Router error: {str(e)}")
#         return [{"error": f"API Router error: {str(e)}"}]

# def data_analysis_step(user_input, clean_data_array, api_name=None, api_parameters=None):
#     """
#     Enhanced data analysis with truncation detection.

#     Args:
#         user_input (str): User's query
#         clean_data_array (list): Clean array of data (list of objects OR single nested object)
#         api_name (str): Name of the API that was called
#         api_parameters (dict): Parameters used to filter the data

#     Returns:
#         str: AI analysis response
#     """
#     if api_parameters is None:
#         api_parameters = {}

#     logger.info(f"Starting data analysis with {len(clean_data_array)} records")

#     # Check for potential truncation issues
#     try:
#         data_json = json.dumps(clean_data_array)
#         data_size = len(data_json)
#         logger.info(f"Total data size: {data_size} characters")

#         # Check if data might be too large for AI context
#         if data_size > 200000:  # 200k characters
#             logger.warning("Data size exceeds safe limits - truncation likely")
#         elif data_size > 100000:  # 100k characters
#             logger.warning("Data size is very large - potential truncation risk")
#         else:
#             logger.info("Data size is within safe limits")

#         # Test if we can recreate the JSON properly
#         reconstructed = json.loads(data_json)
#         if len(reconstructed) != len(clean_data_array):
#             logger.error(f"JSON reconstruction failed. Original: {len(clean_data_array)}, Reconstructed: {len(reconstructed)}")
#         else:
#             logger.info(f"JSON reconstruction successful - {len(reconstructed)} records")

#     except Exception as e:
#         logger.error(f"JSON processing failed: {str(e)}")

#     # Show first and last few records to verify completeness
#     if len(clean_data_array) > 0:
#         first_item = clean_data_array[0]
#         if isinstance(first_item, dict):
#             if any(key in first_item for key in ["Overall Details", "Asset Details", "CWI and NDE Result Details"]):
#                 logger.info(f"Processing nested object structure for GetDetailsbyWeldSerialNumber")
#             else:
#                 first_id = first_item.get('TransmissionWorkOrderID', 'N/A')
#                 last_id = clean_data_array[-1].get('TransmissionWorkOrderID', 'N/A') if isinstance(clean_data_array[-1], dict) else 'N/A'
#                 sample_ids = [wo.get('TransmissionWorkOrderID', 'N/A') for wo in clean_data_array[:5] if isinstance(wo, dict)]
#                 logger.info(f"Data range - First ID: {first_id}, Last ID: {last_id}, Sample IDs: {sample_ids}")

#     analysis_prompt = get_data_analysis_prompt(user_input, clean_data_array, api_name, api_parameters)

#     # Check prompt size
#     prompt_size = len(analysis_prompt)
#     logger.info(f"Analysis prompt size: {prompt_size} characters")
#     if prompt_size > 150000:
#         logger.warning("Prompt size is very large - may cause AI processing issues")

#     messages = [
#         {
#             "role": "system",
#             "content": analysis_prompt
#         },
#         {
#             "role": "user",
#             "content": f"Analyze the complete dataset to answer: {user_input}"
#         }
#     ]

#     try:
#         response = azure_client.chat.completions.create(
#             model=azureopenai,
#             messages=messages,
#             temperature=0.0  # Zero temperature for precise data analysis and counting
#         )
#         ai_response = response.choices[0].message.content

#         logger.info("Data analysis completed successfully")

#         # Try to extract count from AI response for verification
#         import re
#         count_matches = re.findall(r'\b(\d+)\b', ai_response)
#         if count_matches:
#             logger.info(f"Numbers found in AI response: {count_matches}, Expected count: {len(clean_data_array)}")

#         return ai_response

#     except Exception as e:
#         logger.error(f"AI processing failed: {str(e)}")
#         return f"Data Analysis error: {str(e)}"

# def handle_weldinsights(user_input, auth_token=None):
#     """
#     Main WeldInsights handler that processes user queries through API routing and data analysis.

#     Args:
#         user_input (str): User's query about work orders
#         auth_token (str, optional): Authentication token for API calls

#     Returns:
#         str: Processed response from data analysis
#     """
#     try:
#         logger.info("Step 1: API Router - Fetching data...")
#         # Step 1: Get raw data from APIs
#         api_results = api_router_step(user_input, auth_token)

#         # Handle clarification requests from API router
#         if api_results and len(api_results) == 1 and "clarification" in api_results[0]:
#             return api_results[0]["clarification"]

#         if not api_results or (len(api_results) == 1 and "error" in api_results[0]):
#             return api_results[0].get("error", "No data retrieved from APIs")

#         # Log API results structure for debugging
#         logger.info(f"Received {len(api_results)} API results")
#         for i, result in enumerate(api_results):
#             if "data" in result and isinstance(result["data"], dict):
#                 nested_data = result["data"].get("data", {})
#                 if isinstance(nested_data, dict) and "Data" in nested_data:
#                     data_obj = nested_data["Data"]
#                     if data_obj is not None and isinstance(data_obj, (list, str)):
#                         data_length = len(data_obj)
#                         logger.info(f"API Result {i+1}: Contains {data_length} data objects")
#                     else:
#                         logger.info(f"API Result {i+1}: Data field is {type(data_obj)}")

#         logger.info("Step 1.5: Extracting clean data...")
#         # Extract clean data (handles both array and nested object patterns)
#         clean_data_array = extract_clean_data(api_results)

#         # NEW: Deduplicate if multiple API calls were made
#         if len(api_results) > 1:
#             logger.info(f"Multiple API calls detected ({len(api_results)} calls), applying deduplication...")
#             clean_data_array = deduplicate_data_by_json(clean_data_array)

#         # Extract API name and parameters from first result
#         api_name = api_results[0].get("api_name", "Unknown") if api_results else "Unknown"
#         api_parameters = api_results[0].get("parameters", {}) if api_results else {}
#         logger.info(f"Processing data for API: {api_name}")

#         if not clean_data_array:
#             logger.warning("No clean data extracted. No records found matching the criteria.")
#             # Pass empty array to data analysis to handle "no data found" case properly
#             final_response = data_analysis_step(user_input, [], api_name, api_parameters)
#             return final_response

#         logger.info("Step 2: Data Analysis - Analyzing clean data...")
#         # Step 2: Analyze the clean data array
#         final_response = data_analysis_step(user_input, clean_data_array, api_name, api_parameters)

#         return final_response

#     except Exception as e:
#         logger.error(f"WeldInsights processing failed: {str(e)}")
#         return f"Error in WeldInsights two-step processing: {str(e)}"

# import os, json
# import logging
# import re

# # New Imports from our refactored solution
# from utils.data_extractor import extract_clean_data
# from utils.data_transformers import get_transformer
# from prompts.weld_analysis_prompt import get_data_analysis_prompt
# from prompts.weld_apis_prompts.common_prompt import get_no_data_prompt 

# from config.azure_client import get_azure_chat_openai
# from tools.execute_api import execute_api
# from tools.weldinsights_tools import get_weldinsights_tools
# from prompts.weld_api_router_prompt import get_api_router_prompt

# logger = logging.getLogger(__name__)

# # Initialize Azure OpenAI client
# try:
#     azure_client, azureopenai = get_azure_chat_openai()
#     logger.info("Azure OpenAI client initialized for WeldInsights agent")
# except Exception as e:
#     logger.error(f"Failed to initialize Azure OpenAI client in WeldInsights agent: {str(e)}")
#     azure_client, azureopenai = None, None

# # All other helper functions remain largely the same, but they now rely on the new data_extractor.
# # execute_weldinsights_tool_call, execute_multi_api_calls, deduplicate_data_by_json
# # ... (insert the code for these functions from your original file) ...

# def execute_weldinsights_tool_call(tool_call, auth_token=None):
#     function_name = tool_call.function.name
#     arguments = json.loads(tool_call.function.arguments)
#     api_path = arguments.pop("api_path", "AITransmissionWorkOrder")
#     parameters = {k: v for k, v in arguments.items() if v is not None}
#     logger.info(f"Executing WeldInsights tool: {function_name}")
#     try:
#         result = execute_api(api_path, function_name, parameters, auth_token, method="POST")
#         logger.info(f"WeldInsights tool {function_name} executed successfully")
#         return result
#     except Exception as e:
#         logger.error(f"WeldInsights tool {function_name} failed: {str(e)}")
#         return {"error": f"Tool execution failed: {str(e)}"}

# def execute_multi_api_calls(calls, auth_token=None):
#     api_results = []
#     warnings = []
#     for i, call in enumerate(calls, 1):
#         function_name = call.get("function_name")
#         parameters = call.get("parameters", {})
#         logger.info(f"Multi-call {i}/{len(calls)}: Executing {function_name} with parameters {parameters}")
#         try:
#             result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")
#             api_results.append({
#                 "api_name": function_name,
#                 "parameters": parameters,
#                 "data": result
#             })
#             logger.info(f"Multi-call {i}/{len(calls)}: Success")
#         except Exception as e:
#             logger.error(f"Multi-call {i}/{len(calls)}: Failed - {str(e)}")
#             warnings.append(f"Call {i} failed: {str(e)}")
#     if warnings:
#         logger.warning(f"Multi-call completed with {len(warnings)} failures: {warnings}")
#     return api_results

# def deduplicate_data_by_json(clean_data_array):
#     if not clean_data_array:
#         return clean_data_array
#     seen_json_keys = set()
#     deduplicated = []
#     for item in clean_data_array:
#         if isinstance(item, dict):
#             json_key = json.dumps(item, sort_keys=True)
#             if json_key not in seen_json_keys:
#                 seen_json_keys.add(json_key)
#                 deduplicated.append(item)
#         else:
#             deduplicated.append(item)
#     duplicates_removed = len(clean_data_array) - len(deduplicated)
#     if duplicates_removed > 0:
#         logger.info(f"Deduplication: Removed {duplicates_removed} duplicate records using JSON stringify")
#     return deduplicated

# def api_router_step(user_input, auth_token=None):
#     router_prompt = get_api_router_prompt(user_input)
#     messages = [
#         {
#             "role": "system",
#             "content": router_prompt
#         },
#         {
#             "role": "user",
#             "content": user_input
#         }
#     ]
#     try:
#         response = azure_client.chat.completions.create(
#             model=azureopenai,
#             messages=messages,
#             tools=get_weldinsights_tools(),
#             tool_choice="auto",
#             temperature=0.0
#         )
#         response_content = response.choices[0].message.content
#         if response_content:
#             logger.info(f"LLM Response Content: {response_content}")
#         if response.choices[0].message.tool_calls:
#             logger.info(f"LLM selected {len(response.choices[0].message.tool_calls)} tool(s) to call:")
#             for i, tool_call in enumerate(response.choices[0].message.tool_calls, 1):
#                 logger.info(f"Tool {i}: {tool_call.function.name}")
#                 try:
#                     params = json.loads(tool_call.function.arguments)
#                     param_summary = {k: f"<{type(v).__name__}>" if isinstance(v, (list, dict)) and len(str(v)) > 100 else v
#                                      for k, v in params.items()}
#                     logger.info(f"Tool {i} Parameters: {param_summary}")
#                 except:
#                     logger.info(f"Tool {i} Parameters: <unparseable>")
#         else:
#             logger.info("LLM made no tool calls")
#         logger.info("=== END API ROUTER DECISION ===")
#         if not response.choices[0].message.tool_calls:
#             clarification_response = response.choices[0].message.content
#             if clarification_response:
#                 try:
#                     content = clarification_response.strip()
#                     if "```json" in content:
#                         start = content.find("```json") + 7
#                         end = content.find("```", start)
#                         if end > start:
#                             content = content[start:end].strip()
#                     elif content.startswith('{') and content.endswith('}'):
#                         pass
#                     else:
#                         lines = content.split('\n')
#                         for line in lines:
#                             line = line.strip()
#                             if line.startswith('{') and line.endswith('}'):
#                                 content = line
#                                 break
#                     parsed_response = json.loads(content)
#                     if isinstance(parsed_response, dict) and "type" in parsed_response:
#                         response_type = parsed_response["type"]
#                         if response_type == "api_call":
#                             if "calls" in parsed_response and isinstance(parsed_response["calls"], list):
#                                 calls = parsed_response["calls"]
#                                 logger.info(f"LLM provided multi-call format with {len(calls)} calls")
#                                 api_results = execute_multi_api_calls(calls, auth_token)
#                                 return api_results
#                             else:
#                                 function_name = parsed_response.get("function_name")
#                                 parameters = parsed_response.get("parameters", {})
#                                 logger.info(f"LLM provided consistent API call format: {function_name} with params {parameters}")
#                                 tool_result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")
#                                 return [{
#                                     "api_name": function_name,
#                                     "parameters": parameters,
#                                     "data": tool_result
#                                 }]
#                         elif response_type == "clarification":
#                             clarification_message = parsed_response.get("message", "")
#                             logger.info("LLM provided consistent clarification format")
#                             return [{"clarification": clarification_message}]
#                     elif isinstance(parsed_response, dict):
#                         if "name" in parsed_response and "arguments" in parsed_response:
#                             function_name = parsed_response["name"]
#                             if function_name.startswith("functions."):
#                                 function_name = function_name[10:]
#                             arguments = parsed_response["arguments"]
#                             logger.info(f"LLM provided legacy tool call format: {function_name} with args {arguments}")
#                             tool_result = execute_api("AITransmissionWorkOrder", function_name, arguments, auth_token, method="POST")
#                             return [{
#                                 "api_name": function_name,
#                                 "parameters": arguments,
#                                 "data": tool_result
#                             }]
#                         elif any(key in parsed_response for key in ['ContractorName', 'ContractorCWIName', 'ContractorNDEName', 'ContractorCRIName']):
#                             logger.info(f"LLM provided legacy parameters format: {parsed_response}")
#                             tool_result = execute_api("AITransmissionWorkOrder", "GetWorkOrderInformation", parsed_response, auth_token, method="POST")
#                             return [{
#                                 "api_name": "GetWorkOrderInformation",
#                                 "parameters": parsed_response,
#                                 "data": tool_result
#                             }]
#                 except json.JSONDecodeError as e:
#                     logger.warning(f"Failed to parse JSON response: {e}")
#                 except Exception as e:
#                     logger.warning(f"Error processing response format: {e}")
#                 logger.info("LLM provided plain text clarification")
#                 return [{"clarification": clarification_response}]
#             else:
#                 logger.warning("LLM made no tool calls and provided no content")
#                 return [{"error": "No tools selected and no clarification provided"}]
#         api_results = []
#         for tool_call in response.choices[0].message.tool_calls:
#             logger.info(f"Step 1 - Executing tool: {tool_call.function.name}")
#             tool_result = execute_weldinsights_tool_call(tool_call, auth_token)
#             api_results.append({
#                 "api_name": tool_call.function.name,
#                 "parameters": json.loads(tool_call.function.arguments),
#                 "data": tool_result
#             })
#         return api_results
#     except Exception as e:
#         logger.error(f"API Router error: {str(e)}")
#         return [{"error": f"API Router error: {str(e)}"}]
        
# def data_analysis_step(user_input, clean_data_array, api_name=None, api_parameters=None, is_follow_up=False):
#     """
#     Orchestrates the data transformation and AI analysis. This is the main refactored function.
    
#     Args:
#         user_input (str): User's query.
#         clean_data_array (list): Clean data array extracted from the API response.
#         api_name (str): Name of the API called.
#         api_parameters (dict): Parameters used for the API call.
#         is_follow_up (bool): Flag indicating if this is a follow-up request.
    
#     Returns:
#         str: AI analysis response.
#     """
#     if api_parameters is None:
#         api_parameters = {}
        
#     logger.info(f"Starting data analysis for API: {api_name} with {len(clean_data_array)} records.")
    
#     # Get the appropriate data transformer based on the API name
#     transformer = get_transformer(api_name)
    
#     if transformer:
#         analysis_results = transformer(clean_data_array, api_parameters)
#     else:
#         # Fallback for APIs without a dedicated transformer
#         analysis_results = {
#             "total_records": len(clean_data_array),
#             "raw_data": clean_data_array,
#             "filter_applied": api_parameters
#         }

#     # Handle the "no data found" case first
#     total_records = analysis_results.get("total_records", 0)
#     if total_records == 0:
#         logger.warning("No clean data extracted. No records found matching the criteria.")
#         no_data_prompt = get_no_data_prompt(user_input, api_parameters)
#         messages = [{"role": "system", "content": no_data_prompt}]
#         try:
#             response = azure_client.chat.completions.create(model=azureopenai, messages=messages, temperature=0.0)
#             return response.choices[0].message.content
#         except Exception as e:
#             logger.error(f"AI processing for no data prompt failed: {str(e)}")
#             return f"No records found for the specified criteria. (AI error: {str(e)})"
            
#     # Build the AI prompt using the pre-processed data
#     analysis_prompt = get_data_analysis_prompt(user_input, analysis_results, api_name, is_follow_up)
    
#     messages = [
#         {"role": "system", "content": analysis_prompt},
#         {"role": "user", "content": f"Analyze the data to answer: {user_input}"}
#     ]
    
#     try:
#         response = azure_client.chat.completions.create(
#             model=azureopenai,
#             messages=messages,
#             temperature=0.0
#         )
#         ai_response = response.choices[0].message.content
#         logger.info("Data analysis completed successfully.")
        
#         # Optional: Log AI response details for debugging
#         count_matches = re.findall(r'\b(\d+)\b', ai_response)
#         if count_matches:
#             logger.info(f"Numbers found in AI response: {count_matches}, Expected count: {total_records}")
            
#         return ai_response
#     except Exception as e:
#         logger.error(f"AI processing failed: {str(e)}")
#         return f"Data Analysis error: {str(e)}"

# # ... (all imports and other functions remain the same) ...

# def handle_weldinsights(user_input, auth_token=None, is_follow_up=False):
#     """
#     Main WeldInsights handler that processes user queries through API routing and data analysis.
    
#     Args:
#         user_input (str): User's query about work orders
#         auth_token (str, optional): Authentication token for API calls
#         is_follow_up (bool): Flag indicating if this is a follow-up request.
    
#     Returns:
#         str: Processed response from data analysis
#     """
#     try:
#         # Step 1: Get data from APIs
#         if is_follow_up:
#             # For a real application, you'd retrieve cached results here to avoid re-calling the API.
#             # This example keeps it simple by always calling the API.
#             logger.info("Follow-up request detected. Re-fetching data for analysis.")
#             api_results = api_router_step(user_input, auth_token)
#         else:
#             logger.info("Step 1: API Router - Fetching data...")
#             api_results = api_router_step(user_input, auth_token)

#         if api_results and len(api_results) == 1 and "clarification" in api_results[0]:
#             return api_results[0]["clarification"]

#         if not api_results or (len(api_results) == 1 and "error" in api_results[0]):
#             return api_results[0].get("error", "No data retrieved from APIs")

#         logger.info("Step 1.5: Extracting clean data...")
#         clean_data_array = extract_clean_data(api_results)

#         if len(api_results) > 1:
#             logger.info(f"Multiple API calls detected ({len(api_results)} calls), applying deduplication...")
#             clean_data_array = deduplicate_data_by_json(clean_data_array)
            
#         api_name = api_results[0].get("api_name", "Unknown") if api_results else "Unknown"
#         api_parameters = api_results[0].get("parameters", {}) if api_results else {}
#         logger.info(f"Processing data for API: {api_name}")

#         logger.info("Step 2: Data Analysis - Analyzing clean data...")
#         # Pass the clean data array and the follow-up flag to the analysis step
#         final_response = data_analysis_step(user_input, clean_data_array, api_name, api_parameters, is_follow_up)

#         return final_response
            
#     except Exception as e:
#         logger.error(f"WeldInsights processing failed: {str(e)}")
#         return f"Error in WeldInsights two-step processing: {str(e)}"


# import os, json
# import logging
# import re

# # New Imports from our refactored solution
# from utils.data_extractor import extract_clean_data
# from utils.data_transformers import get_transformer
# from prompts.weld_analysis_prompt import get_data_analysis_prompt
# from prompts.weld_apis_prompts.common_prompt import get_no_data_prompt 

# from config.azure_client import get_azure_chat_openai
# from tools.execute_api import execute_api
# from tools.weldinsights_tools import get_weldinsights_tools
# from prompts.weld_api_router_prompt import get_api_router_prompt

# logger = logging.getLogger(__name__)

# # Initialize Azure OpenAI client
# try:
#     azure_client, azureopenai = get_azure_chat_openai()
#     logger.info("Azure OpenAI client initialized for WeldInsights agent")
# except Exception as e:
#     logger.error(f"Failed to initialize Azure OpenAI client in WeldInsights agent: {str(e)}")
#     azure_client, azureopenai = None, None

# def execute_weldinsights_tool_call(tool_call, auth_token=None):
#     function_name = tool_call.function.name
#     arguments = json.loads(tool_call.function.arguments)
#     api_path = arguments.pop("api_path", "AITransmissionWorkOrder")
#     parameters = {k: v for k, v in arguments.items() if v is not None}
#     logger.info(f"Executing WeldInsights tool: {function_name}")
#     try:
#         result = execute_api(api_path, function_name, parameters, auth_token, method="POST")
#         logger.info(f"WeldInsights tool {function_name} executed successfully")
#         return result
#     except Exception as e:
#         logger.error(f"WeldInsights tool {function_name} failed: {str(e)}")
#         return {"error": f"Tool execution failed: {str(e)}"}

# def execute_multi_api_calls(calls, auth_token=None):
#     api_results = []
#     warnings = []
#     for i, call in enumerate(calls, 1):
#         function_name = call.get("function_name")
#         parameters = call.get("parameters", {})
#         logger.info(f"Multi-call {i}/{len(calls)}: Executing {function_name} with parameters {parameters}")
#         try:
#             result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")
#             api_results.append({
#                 "api_name": function_name,
#                 "parameters": parameters,
#                 "data": result
#             })
#             logger.info(f"Multi-call {i}/{len(calls)}: Success")
#         except Exception as e:
#             logger.error(f"Multi-call {i}/{len(calls)}: Failed - {str(e)}")
#             warnings.append(f"Call {i} failed: {str(e)}")
#     if warnings:
#         logger.warning(f"Multi-call completed with {len(warnings)} failures: {warnings}")
#     return api_results

# def deduplicate_data_by_json(clean_data_array):
#     if not clean_data_array:
#         return clean_data_array
#     seen_json_keys = set()
#     deduplicated = []
#     for item in clean_data_array:
#         if isinstance(item, dict):
#             json_key = json.dumps(item, sort_keys=True)
#             if json_key not in seen_json_keys:
#                 seen_json_keys.add(json_key)
#                 deduplicated.append(item)
#         else:
#             deduplicated.append(item)
#     duplicates_removed = len(clean_data_array) - len(deduplicated)
#     if duplicates_removed > 0:
#         logger.info(f"Deduplication: Removed {duplicates_removed} duplicate records using JSON stringify")
#     return deduplicated

# def api_router_step(user_input, auth_token=None):
#     router_prompt = get_api_router_prompt(user_input)
#     messages = [
#         {
#             "role": "system",
#             "content": router_prompt
#         },
#         {
#             "role": "user",
#             "content": user_input
#         }
#     ]
#     try:
#         response = azure_client.chat.completions.create(
#             model=azureopenai,
#             messages=messages,
#             tools=get_weldinsights_tools(),
#             tool_choice="auto",
#             temperature=0.0
#         )
#         response_content = response.choices[0].message.content
#         if response_content:
#             logger.info(f"LLM Response Content: {response_content}")
#         if response.choices[0].message.tool_calls:
#             logger.info(f"LLM selected {len(response.choices[0].message.tool_calls)} tool(s) to call:")
#             for i, tool_call in enumerate(response.choices[0].message.tool_calls, 1):
#                 logger.info(f"Tool {i}: {tool_call.function.name}")
#                 try:
#                     params = json.loads(tool_call.function.arguments)
#                     param_summary = {k: f"<{type(v).__name__}>" if isinstance(v, (list, dict)) and len(str(v)) > 100 else v
#                                      for k, v in params.items()}
#                     logger.info(f"Tool {i} Parameters: {param_summary}")
#                 except:
#                     logger.info(f"Tool {i} Parameters: <unparseable>")
#         else:
#             logger.info("LLM made no tool calls")
#         logger.info("=== END API ROUTER DECISION ===")
#         if not response.choices[0].message.tool_calls:
#             clarification_response = response.choices[0].message.content
#             if clarification_response:
#                 try:
#                     content = clarification_response.strip()
#                     if "```json" in content:
#                         start = content.find("```json") + 7
#                         end = content.find("```", start)
#                         if end > start:
#                             content = content[start:end].strip()
#                     elif content.startswith('{') and content.endswith('}'):
#                         pass
#                     else:
#                         lines = content.split('\n')
#                         for line in lines:
#                             line = line.strip()
#                             if line.startswith('{') and line.endswith('}'):
#                                 content = line
#                                 break
#                     parsed_response = json.loads(content)
#                     if isinstance(parsed_response, dict) and "type" in parsed_response:
#                         response_type = parsed_response["type"]
#                         if response_type == "api_call":
#                             if "calls" in parsed_response and isinstance(parsed_response["calls"], list):
#                                 calls = parsed_response["calls"]
#                                 logger.info(f"LLM provided multi-call format with {len(calls)} calls")
#                                 api_results = execute_multi_api_calls(calls, auth_token)
#                                 return api_results
#                             else:
#                                 function_name = parsed_response.get("function_name")
#                                 parameters = parsed_response.get("parameters", {})
#                                 logger.info(f"LLM provided consistent API call format: {function_name} with params {parameters}")
#                                 tool_result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")
#                                 return [{
#                                     "api_name": function_name,
#                                     "parameters": parameters,
#                                     "data": tool_result
#                                 }]
#                         elif response_type == "clarification":
#                             clarification_message = parsed_response.get("message", "")
#                             logger.info("LLM provided consistent clarification format")
#                             return [{"clarification": clarification_message}]
#                     elif isinstance(parsed_response, dict):
#                         if "name" in parsed_response and "arguments" in parsed_response:
#                             function_name = parsed_response["name"]
#                             if function_name.startswith("functions."):
#                                 function_name = function_name[10:]
#                             arguments = parsed_response["arguments"]
#                             logger.info(f"LLM provided legacy tool call format: {function_name} with args {arguments}")
#                             tool_result = execute_api("AITransmissionWorkOrder", function_name, arguments, auth_token, method="POST")
#                             return [{
#                                 "api_name": function_name,
#                                 "parameters": arguments,
#                                 "data": tool_result
#                             }]
#                         elif any(key in parsed_response for key in ['ContractorName', 'ContractorCWIName', 'ContractorNDEName', 'ContractorCRIName']):
#                             logger.info(f"LLM provided legacy parameters format: {parsed_response}")
#                             tool_result = execute_api("AITransmissionWorkOrder", "GetWorkOrderInformation", parsed_response, auth_token, method="POST")
#                             return [{
#                                 "api_name": "GetWorkOrderInformation",
#                                 "parameters": parsed_response,
#                                 "data": tool_result
#                             }]
#                 except json.JSONDecodeError as e:
#                     logger.warning(f"Failed to parse JSON response: {e}")
#                 except Exception as e:
#                     logger.warning(f"Error processing response format: {e}")
#                 logger.info("LLM provided plain text clarification")
#                 return [{"clarification": clarification_response}]
#             else:
#                 logger.warning("LLM made no tool calls and provided no content")
#                 return [{"error": "No tools selected and no clarification provided"}]
#         api_results = []
#         for tool_call in response.choices[0].message.tool_calls:
#             logger.info(f"Step 1 - Executing tool: {tool_call.function.name}")
#             tool_result = execute_weldinsights_tool_call(tool_call, auth_token)
#             api_results.append({
#                 "api_name": tool_call.function.name,
#                 "parameters": json.loads(tool_call.function.arguments),
#                 "data": tool_result
#             })
#         return api_results
#     except Exception as e:
#         logger.error(f"API Router error: {str(e)}")
#         return [{"error": f"API Router error: {str(e)}"}]
        
# def data_analysis_step(user_input, clean_data_array, api_name=None, api_parameters=None, is_follow_up=False):
#     if api_parameters is None:
#         api_parameters = {}
        
#     logger.info(f"Starting data analysis for API: {api_name} with {len(clean_data_array)} records.")
    
#     transformer = get_transformer(api_name)
    
#     if transformer:
#         analysis_results = transformer(clean_data_array, api_parameters)
#     else:
#         analysis_results = {
#             "total_records": len(clean_data_array),
#             "raw_data": clean_data_array,
#             "filter_applied": api_parameters
#         }

#     # --- CRITICAL FIX: Use the calculated total from the transformer ---
#     total_records = analysis_results.get("total_records", 0)
    
#     if total_records == 0:
#         logger.warning("No clean data extracted. No records found matching the criteria.")
#         no_data_prompt = get_no_data_prompt(user_input, api_parameters)
#         messages = [{"role": "system", "content": no_data_prompt}]
#         try:
#             response = azure_client.chat.completions.create(model=azureopenai, messages=messages, temperature=0.0)
#             return response.choices[0].message.content
#         except Exception as e:
#             logger.error(f"AI processing for no data prompt failed: {str(e)}")
#             return f"No records found for the specified criteria. (AI error: {str(e)})"
            
#     # Build the AI prompt using the pre-processed data
#     analysis_prompt = get_data_analysis_prompt(user_input, analysis_results, api_name, is_follow_up)
    
#     messages = [
#         {"role": "system", "content": analysis_prompt},
#         {"role": "user", "content": f"Analyze the data to answer: {user_input}"}
#     ]
    
#     try:
#         response = azure_client.chat.completions.create(
#             model=azureopenai,
#             messages=messages,
#             temperature=0.0
#         )
#         ai_response = response.choices[0].message.content
#         logger.info("Data analysis completed successfully.")
        
#         count_matches = re.findall(r'\b(\d+)\b', ai_response)
#         if count_matches:
#             logger.info(f"Numbers found in AI response: {count_matches}, Expected count: {total_records}")
            
#         return ai_response
#     except Exception as e:
#         logger.error(f"AI processing failed: {str(e)}")
#         return f"Data Analysis error: {str(e)}"

# def handle_weldinsights(user_input, auth_token=None, is_follow_up=False):
#     try:
#         if is_follow_up:
#             logger.info("Follow-up request detected. Re-fetching data for analysis.")
#             api_results = api_router_step(user_input, auth_token)
#         else:
#             logger.info("Step 1: API Router - Fetching data...")
#             api_results = api_router_step(user_input, auth_token)

#         if api_results and len(api_results) == 1 and "clarification" in api_results[0]:
#             return api_results[0]["clarification"]

#         if not api_results or (len(api_results) == 1 and "error" in api_results[0]):
#             return api_results[0].get("error", "No data retrieved from APIs")

#         logger.info("Step 1.5: Extracting clean data...")
#         clean_data_array = extract_clean_data(api_results)

#         if len(api_results) > 1:
#             logger.info(f"Multiple API calls detected ({len(api_results)} calls), applying deduplication...")
#             clean_data_array = deduplicate_data_by_json(clean_data_array)
            
#         api_name = api_results[0].get("api_name", "Unknown") if api_results else "Unknown"
#         api_parameters = api_results[0].get("parameters", {}) if api_results else {}
#         logger.info(f"Processing data for API: {api_name}")

#         logger.info("Step 2: Data Analysis - Analyzing clean data...")
#         final_response = data_analysis_step(user_input, clean_data_array, api_name, api_parameters, is_follow_up)

#         return final_response
            
#     except Exception as e:
#         logger.error(f"WeldInsights processing failed: {str(e)}")
#         return f"Error in WeldInsights two-step processing: {str(e)}"

# # --- END weldinsight_agent.py ---











import os, json
import logging
import re

# New Imports from our refactored solution
from utils.data_extractor import extract_clean_data
from utils.data_transformers import get_transformer
from prompts.weld_analysis_prompt import get_data_analysis_prompt
from prompts.weld_apis_prompts.common_prompt import get_no_data_prompt 

from config.azure_client import get_azure_chat_openai
from tools.execute_api import execute_api
from tools.weldinsights_tools import get_weldinsights_tools
from prompts.weld_api_router_prompt import get_api_router_prompt

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
    Dynamically executes tool functions from weldinsights_tools.py.
    This allows each tool to handle its own logic (API call or orchestration).
    """
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    logger.info(f"Executing WeldInsights tool: {function_name}")

    try:
        # Dynamically import and call the tool function
        import tools.weldinsights_tools as tools_module

        if hasattr(tools_module, function_name):
            tool_function = getattr(tools_module, function_name)
            # Call the actual Python function with arguments and auth_token
            result = tool_function(**arguments, auth_token=auth_token)
            logger.info(f"WeldInsights tool {function_name} executed successfully")
            return result
        else:
            error_msg = f"Tool function {function_name} not found in weldinsights_tools"
            logger.error(error_msg)
            return {"error": error_msg}

    except Exception as e:
        logger.error(f"WeldInsights tool {function_name} failed: {str(e)}")
        return {"error": f"Tool execution failed: {str(e)}"}

def execute_multi_api_calls(calls, auth_token=None):
    """
    Execute multiple API calls dynamically using tool functions.
    """
    api_results = []
    warnings = []

    import tools.weldinsights_tools as tools_module

    for i, call in enumerate(calls, 1):
        function_name = call.get("function_name")
        parameters = call.get("parameters", {})
        logger.info(f"Multi-call {i}/{len(calls)}: Executing {function_name} with parameters {parameters}")
        try:
            # Dynamically call the tool function
            if hasattr(tools_module, function_name):
                tool_function = getattr(tools_module, function_name)
                result = tool_function(**parameters, auth_token=auth_token)
            else:
                # Fallback to direct API call if function not found
                result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")

            api_results.append({
                "api_name": function_name,
                "parameters": parameters,
                "data": result
            })
            logger.info(f"Multi-call {i}/{len(calls)}: Success")
        except Exception as e:
            logger.error(f"Multi-call {i}/{len(calls)}: Failed - {str(e)}")
            warnings.append(f"Call {i} failed: {str(e)}")
    if warnings:
        logger.warning(f"Multi-call completed with {len(warnings)} failures: {warnings}")
    return api_results

def deduplicate_data_by_json(clean_data_array):
    if not clean_data_array:
        return clean_data_array
    seen_json_keys = set()
    deduplicated = []
    for item in clean_data_array:
        if isinstance(item, dict):
            json_key = json.dumps(item, sort_keys=True)
            if json_key not in seen_json_keys:
                seen_json_keys.add(json_key)
                deduplicated.append(item)
        else:
            deduplicated.append(item)
    duplicates_removed = len(clean_data_array) - len(deduplicated)
    if duplicates_removed > 0:
        logger.info(f"Deduplication: Removed {duplicates_removed} duplicate records using JSON stringify")
    return deduplicated

def api_router_step(user_input, auth_token=None):
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
        response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=messages,
            tools=get_weldinsights_tools(),
            tool_choice="auto",
            temperature=0.0
        )
        response_content = response.choices[0].message.content
        if response_content:
            logger.info(f"LLM Response Content: {response_content}")
        if response.choices[0].message.tool_calls:
            logger.info(f"LLM selected {len(response.choices[0].message.tool_calls)} tool(s) to call:")
            for i, tool_call in enumerate(response.choices[0].message.tool_calls, 1):
                logger.info(f"Tool {i}: {tool_call.function.name}")
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
        if not response.choices[0].message.tool_calls:
            clarification_response = response.choices[0].message.content
            if clarification_response:
                try:
                    content = clarification_response.strip()
                    if "```json" in content:
                        start = content.find("```json") + 7
                        end = content.find("```", start)
                        if end > start:
                            content = content[start:end].strip()
                    elif content.startswith('{') and content.endswith('}'):
                        pass
                    else:
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
                            if "calls" in parsed_response and isinstance(parsed_response["calls"], list):
                                calls = parsed_response["calls"]
                                logger.info(f"LLM provided multi-call format with {len(calls)} calls")
                                api_results = execute_multi_api_calls(calls, auth_token)
                                return api_results
                            else:
                                function_name = parsed_response.get("function_name")
                                parameters = parsed_response.get("parameters", {})
                                logger.info(f"LLM provided consistent API call format: {function_name} with params {parameters}")

                                # Dynamically call the tool function
                                import tools.weldinsights_tools as tools_module
                                if hasattr(tools_module, function_name):
                                    tool_function = getattr(tools_module, function_name)
                                    tool_result = tool_function(**parameters, auth_token=auth_token)
                                else:
                                    # Fallback to direct API call if function not found
                                    tool_result = execute_api("AITransmissionWorkOrder", function_name, parameters, auth_token, method="POST")

                                return [{
                                    "api_name": function_name,
                                    "parameters": parameters,
                                    "data": tool_result
                                }]
                        elif response_type == "clarification":
                            clarification_message = parsed_response.get("message", "")
                            logger.info("LLM provided consistent clarification format")
                            return [{"clarification": clarification_message}]
                    elif isinstance(parsed_response, dict):
                        if "name" in parsed_response and "arguments" in parsed_response:
                            function_name = parsed_response["name"]
                            if function_name.startswith("functions."):
                                function_name = function_name[10:]
                            arguments = parsed_response["arguments"]
                            logger.info(f"LLM provided legacy tool call format: {function_name} with args {arguments}")

                            # Dynamically call the tool function
                            import tools.weldinsights_tools as tools_module
                            if hasattr(tools_module, function_name):
                                tool_function = getattr(tools_module, function_name)
                                tool_result = tool_function(**arguments, auth_token=auth_token)
                            else:
                                # Fallback to direct API call if function not found
                                tool_result = execute_api("AITransmissionWorkOrder", function_name, arguments, auth_token, method="POST")

                            return [{
                                "api_name": function_name,
                                "parameters": arguments,
                                "data": tool_result
                            }]
                        elif any(key in parsed_response for key in ['ContractorName', 'ContractorCWIName', 'ContractorNDEName', 'ContractorCRIName']):
                            logger.info(f"LLM provided legacy parameters format: {parsed_response}")

                            # Dynamically call GetWorkOrderInformation
                            import tools.weldinsights_tools as tools_module
                            if hasattr(tools_module, 'GetWorkOrderInformation'):
                                tool_function = getattr(tools_module, 'GetWorkOrderInformation')
                                tool_result = tool_function(**parsed_response, auth_token=auth_token)
                            else:
                                # Fallback to direct API call if function not found
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
                logger.info("LLM provided plain text clarification")
                return [{"clarification": clarification_response}]
            else:
                logger.warning("LLM made no tool calls and provided no content")
                return [{"error": "No tools selected and no clarification provided"}]
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
        
def data_analysis_step(user_input, clean_data_array, api_name=None, api_parameters=None, is_follow_up=False):
    if api_parameters is None:
        api_parameters = {}
        
    logger.info(f"Starting data analysis for API: {api_name} with {len(clean_data_array)} records.")
    
    transformer = get_transformer(api_name)
    
    if transformer:
        analysis_results = transformer(clean_data_array, api_parameters)
    else:
        analysis_results = {
            "total_records": len(clean_data_array),
            "raw_data": clean_data_array,
            "filter_applied": api_parameters
        }

    # CRITICAL FIX: Use the calculated total from the transformer. 
    # For grouping APIs, this is typically total_grouped_records, but general APIs use total_records.
    # We must assume the transformer correctly sets the primary count to "total_records" 
    # OR that the transformer for aggregation APIs sets "total_grouped_records".
    # For safety, let's use the field most likely to exist, which is `total_records`.
    total_records = analysis_results.get("total_records", 0)

    # Fallback check for aggregation APIs that might use a specific key like 'total_grouped_records'
    if api_name in ["GetWorkOrderNDEIndicationsbyCriteria", "GetWorkOrderRejactableNDEIndicationsbyCriteria"]:
         total_records = analysis_results.get("total_grouped_records", 0)

    if total_records == 0:
        # The redundant warning line is confirmed to be the source of the confusing log entries.
        # It is removed to avoid misinterpretation of successful data extraction.
        no_data_prompt = get_no_data_prompt(user_input, api_parameters)
        messages = [{"role": "system", "content": no_data_prompt}]
        try:
            response = azure_client.chat.completions.create(model=azureopenai, messages=messages, temperature=0.0)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI processing for no data prompt failed: {str(e)}")
            return f"No records found for the specified criteria. (AI error: {str(e)})"
            
    # Build the AI prompt using the pre-processed data
    analysis_prompt = get_data_analysis_prompt(user_input, analysis_results, api_name, is_follow_up)
    
    messages = [
        {"role": "system", "content": analysis_prompt},
        {"role": "user", "content": f"Analyze the data to answer: {user_input}"}
    ]
    
    try:
        response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=messages,
            temperature=0.0
        )
        ai_response = response.choices[0].message.content
        logger.info("Data analysis completed successfully.")
        
        count_matches = re.findall(r'\b(\d+)\b', ai_response)
        if count_matches:
            logger.info(f"Numbers found in AI response: {count_matches}, Expected count: {total_records}")
            
        return ai_response
    except Exception as e:
        logger.error(f"AI processing failed: {str(e)}")
        return f"Data Analysis error: {str(e)}"

def handle_weldinsights(user_input, auth_token=None, is_follow_up=False):
    try:
        if is_follow_up:
            logger.info("Follow-up request detected. Re-fetching data for analysis.")
            api_results = api_router_step(user_input, auth_token)
        else:
            logger.info("Step 1: API Router - Fetching data...")
            api_results = api_router_step(user_input, auth_token)

        if api_results and len(api_results) == 1 and "clarification" in api_results[0]:
            return api_results[0]["clarification"]

        if not api_results or (len(api_results) == 1 and "error" in api_results[0]):
            return api_results[0].get("error", "No data retrieved from APIs")

        logger.info("Step 1.5: Extracting clean data...")
        clean_data_array = extract_clean_data(api_results)

        if len(api_results) > 1:
            logger.info(f"Multiple API calls detected ({len(api_results)} calls), applying deduplication...")
            clean_data_array = deduplicate_data_by_json(clean_data_array)
            
        api_name = api_results[0].get("api_name", "Unknown") if api_results else "Unknown"
        api_parameters = api_results[0].get("parameters", {}) if api_results else {}
        logger.info(f"Processing data for API: {api_name}")

        logger.info("Step 2: Data Analysis - Analyzing clean data...")
        final_response = data_analysis_step(user_input, clean_data_array, api_name, api_parameters, is_follow_up)

        return final_response
            
    except Exception as e:
        logger.error(f"WeldInsights processing failed: {str(e)}")
        return f"Error in WeldInsights two-step processing: {str(e)}"
