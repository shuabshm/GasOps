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

CRITICAL COUNTING INSTRUCTIONS:

When answering questions about "how many" or counting entities, you MUST use the appropriate count type:

**USE DISTINCT COUNTS when the user asks about unique entities:**
- "How many welds?" → Use `distinct_counts.total_distinct_weld_serial_numbers`
- "How many work orders?" → Use `distinct_counts.total_distinct_work_order_numbers`
- "How many welders?" → Use `distinct_counts.total_distinct_welders`
- "How many projects?" → Use `distinct_counts.total_distinct_project_numbers`
- "How many heat numbers?" → Use `distinct_counts.total_distinct_heat_numbers`
- "How many inspectors?" → Use `distinct_counts.total_distinct_inspectors`
- "How many [any identifier]?" → Use the corresponding distinct count

**USE GROUPED COUNTS (in `counts` section) when the user asks about occurrences or distributions:**
- "How many times does each welder appear?" → Use grouped counts with percentages
- "Show the breakdown by status" → Use distribution counts
- "What's the distribution of indications?" → Use grouped counts

**NEVER use `total_records` for counting unique entities** - it counts rows which may contain duplicates.

**The data structure:**
- `total_records`: Total number of rows/records (may include duplicates)
- `distinct_counts`: Dictionary with distinct/unique counts for each field
- `counts`: Dictionary with occurrence distributions (grouped counts with percentages)

**Example:**
If the data has 100 records but only 75 unique weld serial numbers, then:
- User asks "How many welds?" → Answer: "75 welds" (using distinct count)
- User asks "How many records?" → Answer: "100 records" (using total_records)

**CRITICAL TABLE DISPLAY RULES:**

When presenting results in a tabular format, you MUST sort the data:

1. **Sorting Priority**: ALWAYS sort by the **first column** in the table
2. **Sorting Order**: ALWAYS sort in **descending order** (highest to lowest, Z to A, newest to oldest)
3. **Before Display**: Sort the data array BEFORE creating the table
4. **Consistency**: Maintain the sorted order throughout the entire response

**Examples**:
- If first column is WeldSerialNumber: Sort descending → 250307, 250248, 240931, 240926...
- If first column is Date: Sort descending → 2024-12-31, 2024-12-30, 2024-12-29...
- If first column is ProjectNumber: Sort descending → G-23-901, G-23-900, G-23-899...

**CRITICAL**: Never display unsorted data. Always sort by first column in descending order before displaying any table.

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
