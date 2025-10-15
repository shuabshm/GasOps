def get_common_prompt(user_input, clean_data_array, api_name, filter_context):
    """
    Returns the common prompt section that applies to all WeldInsights APIs

    This prompt contains:
    - Error handling rules
    - Data information
    - Comprehensive analysis methodology

    Args:
        user_input (str): User's question/query
        clean_data_array (list): Clean array of data objects (extracted from API response)
        api_name (str): Name of the API being used
        filter_context (str): Formatted filter parameters string

    Returns:
        str: The formatted common prompt that applies to all APIs
    """
    # Pre-calculate the count
    actual_count = len(clean_data_array)
    aliases = {
        "WorkOrderNumber": ["Work Order," "WR No"],
        "WorkOrderStatusDescription": "Status",
        "WeldSerialNumber": ["Weld Number", "WeldNo", "Joint Id", "Joint number"],
        "Welder": ["Joiner"],
        "HeatNumber": ["Heat No", "Heat #", "Asset", "Asset Number"],
        "ProjectNumber": "Jobnumber"
    }

    return f"""
You are an Expert Data Analysis Agent. Perform comprehensive analysis on the provided JSON data.

You must understand and correctly interpret aliases in the user’s query.
Here are the alias mappings you should use:

ALIASES:
{aliases}

User Question: {user_input}

Data: {clean_data_array}

Dataset Size: {actual_count} records

API Being Used: {api_name}{filter_context}

=== COMMON GUIDELINES (Apply to All APIs) ===

ERROR HANDLING RULES:

**IMPORTANT**: Only apply error handling when {actual_count} == 0 (zero records). If {actual_count} > 0, you have data to analyze and display.

- If the dataset is completely empty ({actual_count} == 0):
  → Respond in natural, human-friendly language by interpreting the user's query intent:
    - Extract the key criteria from the query (e.g., tie-in welds, work order number, specific field values)
    - Craft a response that directly addresses what they were looking for
    Examples:
      User: "Show work orders for John" (when {actual_count} == 0)
      → "There are no work orders where John is assigned."
      User: "Show me welds that were tieinweld in work order 100500514" (when {actual_count} == 0)
      → "There are no tie-in welds in work order 100500514."
      User: "Show production welds with CWI Accept" (when {actual_count} == 0)
      → "There are no production welds with CWI result 'Accept'."

- If the query is unclear or ambiguous:
  → Respond: "Your request is unclear. Could you please rephrase or provide more details?"
- If the query requests more than available records:
  → Respond: "There are only {actual_count} records available, which is less than what you requested."
- If the query refers to unknown fields/terms:
  → Respond in natural language by identifying what was being searched for.
- Always phrase responses naturally, business-friendly, and conversational.
- CRITICAL: Only apply the "no records" error handling when {actual_count} == 0. If {actual_count} > 0, proceed with normal analysis and table display.

DATA INFORMATION:
There are {actual_count} records that were returned by the API after applying the filters shown above. These records represent the results matching the search criteria extracted from the user's question.
**IMPORTANT**: Never use the word "dataset" in your response. Use natural business language like "records", "work orders", "data", "results" instead.

COMPREHENSIVE ANALYSIS METHODOLOGY:
1. **Data Profiling** - Examine structure, fields, and data types
2. **Pattern Analysis** - Identify trends, distributions, and relationships
3. **Quality Assessment** - Check completeness, consistency, and anomalies
4. **Business Intelligence** - Extract actionable insights and recommendations
5. **Statistical Analysis** - Calculate relevant metrics and breakdowns
6. **Temporal Analysis** - Analyze time-based patterns and trends
7. **Geographic Analysis** - Examine regional distributions and patterns
8. **Categorical Analysis** - Break down by status, type, and other categories

=== END COMMON GUIDELINES ===
"""


def get_no_data_prompt(user_input, api_parameters):
    """
    Wrapper function required by weld_insight_agent.py for the 0-record case.
    
    It leverages the existing error-handling logic within get_common_prompt 
    by passing an empty data array, forcing the actual_count to be 0.
    """
    # Pass an empty list to trigger the 0-record logic inside get_common_prompt
    clean_data_array = []
    # Use a placeholder API name since the request failed to retrieve data anyway
    api_name = "NoDataFound"
    filter_context = str(api_parameters)
    
    # Delegate the actual prompt construction to the core function
    return get_common_prompt(user_input, clean_data_array, api_name, filter_context)
