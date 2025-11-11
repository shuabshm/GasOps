# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetNDEReportNumbersbyWorkOrderNumber API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     filter_info = api_parameters if api_parameters else {}

#     return f"""
# === GetNDEReportNumbersbyWorkOrderNumber API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API is a simple listing API that returns all NDE report numbers and their types for a requested work order. This is reference data that users need to look up detailed NDE reports.

# AVAILABLE FIELDS:
# - ReportType: Type of NDE report (e.g., Conventional, Phased Array, Digital Radiography, etc.)
# - NDEReportNumber: NDE report identifier (e.g., NDE2025-00205)

# FIELD DISPLAY RULES:
# **NO smart hiding needed** - Only 2 fields, both are essential:
# - ReportType → ALWAYS show (users need to know what type)
# - NDEReportNumber → ALWAYS show (users need the identifier)

# Always display both fields. Use "-" for null/empty values.

# TABLE SORTING:
# **CRITICAL**: Sort the table by **ReportType (ascending), then NDEReportNumber (ascending)**

# This groups reports by type, making it easy for users to scan.

# **Example:**
# ```
# Report Type        | NDE Report Number
# -------------------|------------------
# Conventional       | NDE2025-00201
# Conventional       | NDE2025-00205
# Conventional       | NDE2025-00210
# Phased Array       | NDE2025-00215
# Phased Array       | NDE2025-00220
# ```

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key insights + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - Display full table with all rows
# - **Skip key insights**

# KEY INSIGHTS GUIDELINES (Super Minimal):
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **What to include (KEEP IT SUPER MINIMAL):**

# 1. **Report type distribution with absolute counts (ONLY insight needed):**
#    - Multiple types: "Report types: 40 Conventional , 5 Phased Array"
#    - Single type: "All reports are Conventional type"
#    - Use absolute counts

# **That's it. NO additional analysis, patterns, trends, or recommendations.**

# **Format Requirements:**
# - Single bullet point for type distribution
# - Use absolute counts
# - Factual observation only
# - Keep concise

# RESPONSE FORMAT:
# 1. **One-sentence answer (Simple - NO type breakdown)**

#    **Format:** "Work order [WorkOrderNumber] has [count] NDE reports"

#    **Examples:**
#    - "Work order 100500514 has 45 NDE reports"
#    - "Work order 100139423 has 8 NDE reports"
#    - "Work order 101351590 has 1 NDE report"

#    Use total record count as the count. Keep it simple - type breakdown goes in key insights.

# 2. **Table Contents** (CONDITIONAL based on response type):
#    - **Initial Response**: DO NOT display any table

#    - **Follow-up Response (when user requests full data)**: Display full table with ALL reports:
#      - Show both fields: ReportType, NDEReportNumber
#      - Sort by: ReportType (ascending), then NDEReportNumber (ascending)
#      - Show ALL reports - no limits
#      - Use clear formatting and handle null values with "-"

# 3. **Key Insights** (CONDITIONAL - skip on follow-up):
#    - **Show key insights** if this is initial response
#    - **Skip key insights** if this is follow-up response to show full data
#    - Follow Super Minimal Guidelines above
#    - Single bullet point with report type distribution
#    - Percentages + absolute counts

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user that they can request the full data
#    - Keep it natural and conversational
#    - Examples: "Would you like to see the full list?", "Need all the reports?", "Should I display the complete data?"
#    - **CRITICAL**: Never use the word "dataset" - use "reports", "list", "data" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "NDE reports", "reports", "list" instead
# - Always show both fields (ReportType and NDEReportNumber)
# - Always sort by ReportType first, then NDEReportNumber
# - **Initial Response: NO TABLE** - just answer + key insights + data request prompt
# - **Follow-up Response: FULL TABLE with ALL rows** - no key insights
# - Key insights: SUPER MINIMAL - just type distribution, nothing more
# - One-sentence answer: Simple format without type breakdown
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, the total is [X] NDE report records. This is a simple reference listing API - keep responses clean and minimal.
# === END GetNDEReportNumbersbyWorkOrderNumber GUIDELINES ===
# """





def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetNDEReportNumbersbyWorkOrderNumber API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetNDEReportNumbersbyWorkOrderNumber API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API is a simple listing API that returns all NDE report numbers and their types for a requested work order. This is reference data that users need to look up detailed NDE reports.

AVAILABLE FIELDS:
- ReportType: Type of NDE report (e.g., Conventional, Phased Array, Digital Radiography, etc.)
- NDEReportNumber: NDE report identifier (e.g., NDE2025-00205)

FIELD DISPLAY RULES:
**NO smart hiding needed** - Only 2 fields, both are essential:
- ReportType → ALWAYS show (users need to know what type)
- NDEReportNumber → ALWAYS show (users need the identifier)

Always display both fields. Use "-" for null/empty values.

TABLE SORTING:
**CRITICAL**: Sort the table by **ReportType (ascending), then NDEReportNumber (ascending)**

This groups reports by type, making it easy for users to scan.

**Example:**
```

Report Type        | NDE Report Number
\-------------------|------------------
Conventional       | NDE2025-00201
Conventional       | NDE2025-00205
Conventional       | NDE2025-00210
Phased Array       | NDE2025-00215
Phased Array       | NDE2025-00220

```

KEY INSIGHTS GUIDELINES (Super Minimal and do not include any heading like "Key Insights" or similar):
**When to show:**
- Show on initial query response (MODE 1)
- Skip on follow-up when user requests full data (MODE 2)

**What to include (KEEP IT SUPER MINIMAL):**

1. **Report type distribution with absolute counts (ONLY insight needed):**
    - Multiple types: "Report types: 40 Conventional , 5 Phased Array"
    - Single type: "All reports are Conventional type"
    - Use absolute counts

**That's it. NO additional analysis, patterns, trends, or recommendations.**

**Format Requirements:**
- Single bullet point for type distribution
- Use absolute counts
- Factual observation only
- Keep concise
- Use absolute counts

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent.

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer (Simple - NO type breakdown):** Provide a concise, direct, one-sentence summary answer.
    * **Format:** "Work order [WorkOrderNumber] has [count] NDE reports"
    * Use total record count as the count.

2.  **Key Insights:** Present the **ONLY** required insight (report type distribution) as a single bullet point, following the **KEY INSIGHTS GUIDELINES** above.

3.  **Data Request Prompt:** Conclude the response with a single-line prompt asking if they want the full data.
    * Examples: "Would you like to see the full list?", "Need all the reports?", "Should I display the complete data?"
    * **CRITICAL**: Never use the word "dataset". **DO NOT** add any other questions or suggestions.

4.  **Table Display:** **STRICTLY DO NOT** display a table in this mode.

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table using phrases like: "show me", "display the data", "yes", "show all", "full data", "full list", or similar.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence confirmation specific to the data being displayed.
    * Example: “Here is the complete list of NDE reports, grouped by type.”

2.  **Key Insights:** **STRICTLY DO NOT** include any key insights.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt or any other unsolicited questions/suggestions.

4.  **Table Display:** Display the full table with **ALL reports**.
    * **Show both fields:** ReportType, NDEReportNumber
    * **Sort by:** ReportType (ascending), then NDEReportNumber (ascending)
    * Use clear formatting and handle null values with "-".

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "NDE reports", "reports", "list" instead
- Always show both fields (ReportType and NDEReportNumber)
- Always sort by ReportType first, then NDEReportNumber
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**
- Key insights: SUPER MINIMAL - just type distribution, nothing more
- One-sentence answer: Simple format without type breakdown

For any counting questions, the total is [X] NDE report records. This is a simple reference listing API - keep responses clean and minimal.
=== END GetNDEReportNumbersbyWorkOrderNumber GUIDELINES ===
"""