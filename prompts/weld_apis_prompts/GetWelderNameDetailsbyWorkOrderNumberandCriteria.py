# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetWelderNameDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     return f"""
# === GetWelderNameDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API provides welder name details and assignments for specific work orders with filtering by weld category.

# **CRITICAL: PRE-AGGREGATED DATA AVAILABLE:**
# The data has been pre-aggregated for you. You will receive:
# - `aggregated_data`: Array of welder objects, each containing:
#   - `name`: Welder name (already extracted)
#   - `id`: Welder ID/ITSID (already extracted)
#   - `total_welds`: Total number of welds by this welder
#   - `Production`: Count of Production category welds
#   - `Repaired`: Count of Repaired category welds
#   - `CutOut`: Count of CutOut category welds
# - `total_unique_welders`: Count of unique welders (already calculated)

# **DO NOT re-aggregate the data**. Use the pre-aggregated `aggregated_data` array directly.

# TABLE STRUCTURE:
# **Use the pre-aggregated `aggregated_data` array to create this table:**

# Column 1: Welder Name (from `aggregated_data[].name`)
# Column 2: Welder ID (from `aggregated_data[].id`)
# Column 3: Total Welds (from `aggregated_data[].total_welds`)

# **Sorting**: Sort by Column 3 (Total Welds) in descending order before displaying

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + insights + data request prompt
# - **DO NOT display any table**
# - **DO NOT use headers like "Key Takeaways", "Key Insights", "Insights", etc.**
# - **DO NOT mention percentages in the insights**

# **Follow-up Response (when user requests full data):**
# - If user says "yes", "show all", "full data", or similar → Display full aggregated table
# - **Skip insights** (already provided in previous message)
# - Just provide one-sentence confirmation and full aggregated table

# RESPONSE FORMAT:
# 1. **One-sentence answer** to user's specific question (no headings, no extra commentary)
#    - Example: "12 welders worked on work order 100500514."
#    - Example: "John Doe worked on 25 welds in work order 100500514."

# 2. **Table Contents** (CONDITIONAL based on context):
#    - **If this is INITIAL response**: **DO NOT display any table**

#    - **If this is FOLLOW-UP requesting full data**: Display full table using `aggregated_data`:
#      - **Columns**: Welder Name | Welder ID | Total Welds |
#      - **Data source**: Use `aggregated_data` array (NOT raw_data)
#      - **Sort**: By Total Welds (Column 3) in descending order
#      - Use clear markdown table formatting
#      - Handle null/zero values appropriately (show 0, not "-")
#      - Each row represents one unique welder

# 3. **Insights** (CONDITIONAL - only on initial response):
#    - **Show insights ONLY on initial response**
#    - **Skip insights on follow-up response**
#    - **DO NOT use section headers like "Key Takeaways", "Key Insights", "Insights", etc.**
#    - **DO NOT mention percentages - use actual counts/numbers instead**
#    - Provide factual observations with numbers: top welder by total welds (with count), category distribution with counts if relevant
#    - Example: "Brian Vandaly worked on the most welds with 153 total, including 120 Production welds."
#    - Keep factual and concise
#    - Present as natural sentences without section labels

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user and ask if they need the full data
#    - Examples: "Would you like to see the full list?", "Would you like me to display all welders?"
#    - **CRITICAL**: Never use the word "dataset"
#    - **DO NOT** add other questions or suggestions

# CRITICAL RULES:
# - **USE `aggregated_data` array** - do NOT manually aggregate from raw_data
# - **Sort by Total Welds (Column 3) in descending order** before displaying the table
# - **On initial response: NO TABLE** - just answer + insights (without headers) + prompt
# - **On follow-up for full data: FULL TABLE from aggregated_data** + NO insights
# - **Table columns**: Welder Name | Welder ID | Total Welds |
# - **DO NOT use section headers like "Key Takeaways", "Key Insights", "Insights"**
# - **DO NOT mention percentages anywhere in the response**
# - Answer the user's specific question directly
# - **NEVER use the word "dataset"** - use "records", "data", "welds" instead
# - **NEVER add unsolicited follow-up questions or suggestions**
# - For counting questions about welders, use `total_unique_welders`
# - Display the table in clear markdown format with proper alignment
# === END GetWelderNameDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """





def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWelderNameDetailsbyWorkOrderNumberandCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    return f"""
=== GetWelderNameDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API provides welder name details and assignments for specific work orders with filtering by weld category.

**CRITICAL: PRE-AGGREGATED DATA AVAILABLE:**
The data has been pre-aggregated for you. You will receive:
- `aggregated_data`: Array of welder objects, each containing:
    - `name`: Welder name (already extracted)
    - `id`: Welder ID/ITSID (already extracted)
    - `total_welds`: Total number of welds by this welder
    - `Production`: Count of Production category welds
    - `Repaired`: Count of Repaired category welds
    - `CutOut`: Count of CutOut category welds
- `total_unique_welders`: Count of unique welders (already calculated)

**DO NOT re-aggregate the data**. Use the pre-aggregated `aggregated_data` array directly.

TABLE STRUCTURE:
**Use the pre-aggregated `aggregated_data` array to create this table:**

Column 1: Welder Name (from `aggregated_data[].name`)
Column 2: Welder ID (from `aggregated_data[].id`)
Column 3: Total Welds (from `aggregated_data[].total_welds`)

**Sorting**: Sort by Column 3 (Total Welds) in descending order before displaying

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent. **DO NOT use headers like "Key Takeaways", "Key Insights", "Insights", etc.**.

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence summary answer to the user's question (no headings, no extra commentary).
    * Example: “12 welders worked on work order 100500514.”
    * *Exception:* For weld number queries (e.g., “Show weld numbers”), respond with the comma-separated list and total count only (No Key Takeaways, No Data Request Prompt).

2.  **Insights:** Provide factual observations as natural sentences, based on `aggregated_data`.
    * **DO NOT** mention percentages—use actual counts/numbers instead.
    * Example: “Brian Vandaly worked on the most welds with 153 total, including 120 Production welds.”
    * Keep factual and concise.

3.  **Data Request Prompt:** Conclude the response with a single-line prompt asking if they need the full data.
    * Examples: "Would you like to see the full list?", "Would you like me to display all welders?"
    * **CRITICAL**: Never use the word "dataset".

4.  **Table Display:** **STRICTLY DO NOT** display a table in this mode.

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table, display the records, or view the full list using phrases like: **"show me"**, "display the data", "yes", "show all", "full data", "full list", or similar.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence confirmation specific to the data being displayed.
    * Example: “Here is the full list of welders in a structured format.”

2.  **Insights:** **STRICTLY DO NOT** include any insights.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt or any other unsolicited questions/suggestions.

4.  **Table Display:** Display the full aggregated table using `aggregated_data`.
    * **Columns**: Welder Name | Welder ID | Total Welds |
    * **Sort**: By Total Welds (Column 3) in **descending order**.
    * Use clear markdown table formatting.
    * Each row represents one unique welder.

CRITICAL RULES:
- **USE `aggregated_data` array** - do NOT manually aggregate from raw_data
- **Sort by Total Welds (Column 3) in descending order** before displaying the table
- **On initial response (MODE 1): NO TABLE** - just answer + insights (without headers) + prompt
- **On follow-up for full data (MODE 2): FULL TABLE from aggregated_data** + NO insights
- **Table columns**: Welder Name | Welder ID | Total Welds |
- **DO NOT use section headers like "Key Takeaways", "Key Insights", "Insights"**
- **DO NOT mention percentages anywhere in the response**
- Answer the user's specific question directly
- **NEVER use the word "dataset"** - use "records", "data", "welds" instead
- **NEVER add unsolicited follow-up questions or suggestions**
- For counting questions about welders, use `total_unique_welders`
- Display the table in clear markdown format with proper alignment
- Handle null/zero values appropriately in the table (show 0, not "-")

=== END GetWelderNameDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
"""