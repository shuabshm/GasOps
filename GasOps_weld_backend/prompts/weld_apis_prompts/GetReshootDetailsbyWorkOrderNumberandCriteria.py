# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetReshootDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     filter_info = api_parameters if api_parameters else {}
    
#     return f"""
# === GetReshootDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API is a workflow/task management API that tracks welds requiring NDE re-inspection (reshoot) and their completion status. Users need to identify pending reshoot work and track accountability.

# AVAILABLE FIELDS:
# - NDEReportNumber: NDE report number with type (e.g., "NDE2025-00205 (Conv)")
# - WeldSerialNumbers: Weld serial number(s) requiring reshoot
# - RequiredReshoot: Whether reshoot is required (Yes/No)
# - UpdateCompleted: Whether update is completed (Yes/No)

# **CRITICAL CONCEPT**: This is quality/rework tracking - welds require NDE re-inspection (reshoot) and users need to track pending vs completed status.

# CORE FIELDS (Workflow Tracking):

# **Always show:**
# - WeldSerialNumbers (which welds need reshoot)
# - NDEReportNumber (which NDE report identified the issue)
# - RequiredReshoot (Yes/No - is reshoot needed?)
# - UpdateCompleted (Yes/No - workflow status)

# **Hide by default:**
# - WorkOrderNumber (always same - already in context)

# SMART FIELD HIDING LOGIC:

# **WorkOrderNumber:** Always hide (same for all records - in input parameter)

# **Core fields:** Always show (even if filtered - context and status matter for workflow tracking)

# ACTION-ORIENTED TABLE SORTING:
# **CRITICAL**: Sort to put action items requiring attention at the top!

# **Primary sort:** RequiredReshoot (descending) → "Yes" first (welds requiring reshoot on top)
# **Secondary sort:** UpdateCompleted (ascending) → "No" first (pending items on top)

# **Result:** Welds requiring reshoot that haven't been completed appear at the very top!

# **Example sorted order:**
# 1. RequiredReshoot=Yes, UpdateCompleted=No (NEEDS ACTION - TOP PRIORITY)
# 2. RequiredReshoot=Yes, UpdateCompleted=Yes (completed reshoots)
# 3. RequiredReshoot=No, UpdateCompleted=No (doesn't need reshoot)
# 4. RequiredReshoot=No, UpdateCompleted=Yes (doesn't need reshoot, updated)

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key insights + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - Display full table with all rows
# - **Skip key insights**

# KEY INSIGHTS GUIDELINES (Workflow-Focused):
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **What to include (workflow tracking focus):**

# 1. **Reshoot status breakdown (ALWAYS include):**
#    - "Reshoot status: 60% completed (9 welds), 40% pending (6 welds)"
#    - If all completed: "All reshoot welds have been completed"
#    - If all pending: "All [X] reshoot welds are still pending completion"
#    - **CRITICAL**: Prominently show pending count - this is what users need for action

# 2. **Required reshoot distribution (if varies):**
#    - "80% require reshoot (12 welds), 20% do not require reshoot (3 welds)"
#    - If all require: "All welds require reshoot (RequiredReshoot=Yes)"
#    - Skip if uniform

# 3. **NDE report distribution (if multiple reports):**
#    - "Reshoots across 3 NDE reports: NDE2025-00205 (8 welds), NDE2025-00210 (5 welds), NDE2025-00215 (2 welds)"
#    - If single report: "All reshoots from single NDE report: NDE2025-00205"

# 4. **Final summary (ONLY if alarming or actionable):**
#    - "10 welds marked for reshoot remain pending for extended period"
#    - "High number of pending reshoots (15+) may require attention"

# **Format Requirements:**
# - Each insight as separate bullet point on its own line
# - Never merge into paragraph
# - Use percentages + absolute counts
# - Factual observations only
# - Focus on actionable information (pending reshoot work)
# - **ONLY state factual observations**
# - **DO NOT include recommendations**

# RESPONSE FORMAT:
# 1. **One-sentence answer (Action-Oriented)**

#    **If pending reshoots > 0 (action needed):**
#    - "[X] welds require reshoot in work order [Y] ([Z] already completed)"
#    - "[X] welds need reshoot in work order [Y]"
#    - Examples:
#      - "10 welds require reshoot in work order 100500514 (5 already completed)"
#      - "15 welds need reshoot in work order 100500514"

#    **If all completed (no action needed):**
#    - "All [X] reshoot welds in work order [Y] have been completed"
#    - Example: "All 15 reshoot welds in work order 100500514 have been completed"

#    **If no reshoots required:**
#    - "No reshoots required for work order [Y]"

#    **Highlight what needs action first!** Use total record count for totals.

# 2. **Table Contents** (CONDITIONAL based on response type):
#    - **Initial Response**: DO NOT display any table

#    - **Follow-up Response (when user requests full data)**: Display full table with ALL records:
#      - Always show: WeldSerialNumbers, NDEReportNumber, RequiredReshoot, UpdateCompleted
#      - Sort by: RequiredReshoot (Yes first), then UpdateCompleted (No first)
#      - Show ALL records - no limits
#      - Use clear formatting and handle null values with "-"

# 3. **Key Insights** (CONDITIONAL - skip on follow-up):
#    - **Show key insights** if this is initial response
#    - **Skip key insights** if this is follow-up response to show full data
#    - Follow Workflow-Focused Guidelines above
#    - Each bullet on its own line
#    - Focus on reshoot status breakdown, NDE report distribution, and actionable information

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user that they can request the full data
#    - Keep it natural and conversational
#    - Examples: "Would you like to see the full details?", "Need the complete list?", "Should I display all reshoot records?"
#    - **CRITICAL**: Never use the word "dataset" - use "reshoot welds", "reshoot records", "list", "data" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "reshoot welds", "reshoot records", "data" instead
# - Always show core fields: WeldSerialNumbers, NDEReportNumber, RequiredReshoot, UpdateCompleted
# - Hide WorkOrderNumber (always same)
# - Sort with action items first (RequiredReshoot=Yes, UpdateCompleted=No on top)
# - **Initial Response: NO TABLE** - just answer + key insights + data request prompt
# - **Follow-up Response: FULL TABLE with ALL rows** - no key insights
# - Key insights: workflow-focused, highlight pending reshoot work prominently
# - One-sentence answer: action-oriented, pending count first if applicable
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, the total is [X] reshoot records. This is a workflow/task management API - focus on actionable information and pending reshoot identification.
# === END GetReshootDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """





# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetReshootDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     filter_info = api_parameters if api_parameters else {}
    
#     return f"""
# === GetReshootDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API is a workflow/task management API that tracks welds requiring NDE re-inspection (reshoot) and their completion status. Users need to identify pending reshoot work and track accountability.

# AVAILABLE FIELDS:
# - NDEReportNumber: NDE report number with type (e.g., "NDE2025-00205 (Conv)")
# - WeldSerialNumbers: Weld serial number(s) requiring reshoot
# - RequiredReshoot: Whether reshoot is required (Yes/No)
# - UpdateCompleted: Whether update is completed (Yes/No)

# **CRITICAL CONCEPT**: This is quality/rework tracking - welds require NDE re-inspection (reshoot) and users need to track pending vs completed status.

# CORE FIELDS (Workflow Tracking):

# **Always show:**
# - WeldSerialNumbers (which welds need reshoot)
# - NDEReportNumber (which NDE report identified the issue)
# - RequiredReshoot (Yes/No - is reshoot needed?)
# - UpdateCompleted (Yes/No - workflow status)

# **Hide by default:**
# - WorkOrderNumber (always same - already in context)

# SMART FIELD HIDING LOGIC:

# **WorkOrderNumber:** Always hide (same for all records - in input parameter)

# **Core fields:** Always show (even if filtered - context and status matter for workflow tracking)

# ACTION-ORIENTED TABLE SORTING:
# **CRITICAL**: Sort to put action items requiring attention at the top!

# **Primary sort:** RequiredReshoot (descending) → "Yes" first (welds requiring reshoot on top)
# **Secondary sort:** UpdateCompleted (ascending) → "No" first (pending items on top)

# **Result:** Welds requiring reshoot that haven't been completed appear at the very top!

# **Example sorted order:**
# 1. RequiredReshoot=Yes, UpdateCompleted=No (NEEDS ACTION - TOP PRIORITY)
# 2. RequiredReshoot=Yes, UpdateCompleted=Yes (completed reshoots)
# 3. RequiredReshoot=No, UpdateCompleted=No (doesn't need reshoot)
# 4. RequiredReshoot=No, UpdateCompleted=Yes (doesn't need reshoot, updated)

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key insights + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - Display full table with all rows
# - **Skip key insights**

# KEY INSIGHTS GUIDELINES (Workflow-Focused):
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **What to include (workflow tracking focus):**

# 1. **Reshoot status breakdown (ALWAYS include):**
#    - "Reshoot status: 60% completed (9 welds), 40% pending (6 welds)"
#    - If all completed: "All reshoot welds have been completed"
#    - If all pending: "All [X] reshoot welds are still pending completion"
#    - **CRITICAL**: Prominently show pending count - this is what users need for action

# 2. **Required reshoot distribution (if varies):**
#    - "80% require reshoot (12 welds), 20% do not require reshoot (3 welds)"
#    - If all require: "All welds require reshoot (RequiredReshoot=Yes)"
#    - Skip if uniform

# 3. **NDE report distribution (if multiple reports):**
#    - "Reshoots across 3 NDE reports: NDE2025-00205 (8 welds), NDE2025-00210 (5 welds), NDE2025-00215 (2 welds)"
#    - If single report: "All reshoots from single NDE report: NDE2025-00205"

# 4. **Final summary (ONLY if alarming or actionable):**
#    - "10 welds marked for reshoot remain pending for extended period"
#    - "High number of pending reshoots (15+) may require attention"

# **Format Requirements:**
# - Each insight as separate bullet point on its own line
# - Never merge into paragraph
# - Use percentages + absolute counts
# - Factual observations only
# - Focus on actionable information (pending reshoot work)
# - **ONLY state factual observations**
# - **DO NOT include recommendations**

# RESPONSE FORMAT:
# 1. **One-sentence answer (Action-Oriented)**

#    **If pending reshoots > 0 (action needed):**
#    - "[X] welds require reshoot in work order [Y] ([Z] already completed)"
#    - "[X] welds need reshoot in work order [Y]"
#    - Examples:
#      - "10 welds require reshoot in work order 100500514 (5 already completed)"
#      - "15 welds need reshoot in work order 100500514"

#    **If all completed (no action needed):**
#    - "All [X] reshoot welds in work order [Y] have been completed"
#    - Example: "All 15 reshoot welds in work order 100500514 have been completed"

#    **If no reshoots required:**
#    - "No reshoots required for work order [Y]"

#    **Highlight what needs action first!** Use total record count for totals.

# 2. **Table Contents** (CONDITIONAL based on response type):
#    - **Initial Response**: DO NOT display any table

#    - **Follow-up Response (when user requests full data)**: Display full table with ALL records:
#      - Always show: WeldSerialNumbers, NDEReportNumber, RequiredReshoot, UpdateCompleted
#      - Sort by: RequiredReshoot (Yes first), then UpdateCompleted (No first)
#      - Show ALL records - no limits
#      - Use clear formatting and handle null values with "-"

# 3. **Key Insights** (CONDITIONAL - skip on follow-up and do not include any heading like "Key Insights" or similar):
#    - **Show key insights** if this is initial response
#    - **Skip key insights** if this is follow-up response to show full data
#    - Follow Workflow-Focused Guidelines above
#    - Each bullet on its own line
#    - Focus on reshoot status breakdown, NDE report distribution, and actionable information (ONLY if alarming or actionable)(always use absolute counts ).

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user that they can request the full data
#    - Keep it natural and conversational
#    - Examples: "Would you like to see the full details?", "Need the complete list?", "Should I display all reshoot records?"
#    - **CRITICAL**: Never use the word "dataset" - use "reshoot welds", "reshoot records", "list", "data" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "reshoot welds", "reshoot records", "data" instead
# - Always show core fields: WeldSerialNumbers, NDEReportNumber, RequiredReshoot, UpdateCompleted
# - Hide WorkOrderNumber (always same)
# - Sort with action items first (RequiredReshoot=Yes, UpdateCompleted=No on top)
# - **Initial Response: NO TABLE** - just answer + key insights + data request prompt
# - **Follow-up Response: FULL TABLE with ALL rows** - no key insights
# - Key insights: workflow-focused, highlight pending reshoot work prominently
# - One-sentence answer: action-oriented, pending count first if applicable
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, the total is [X] reshoot records. This is a workflow/task management API - focus on actionable information and pending reshoot identification.
# === END GetReshootDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """




def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetReshootDetailsbyWorkOrderNumberandCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}
    
    return f"""
=== GetReshootDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API is a workflow/task management API that tracks welds requiring NDE re-inspection (reshoot) and their completion status. Users need to identify pending reshoot work and track accountability.

AVAILABLE FIELDS:
- NDEReportNumber: NDE report number with type (e.g., "NDE2025-00205 (Conv)")
- WeldSerialNumbers: Weld serial number(s) requiring reshoot
- RequiredReshoot: Whether reshoot is required (Yes/No)
- UpdateCompleted: Whether update is completed (Yes/No)

**CRITICAL CONCEPT**: This is quality/rework tracking - welds require NDE re-inspection (reshoot) and users need to track pending vs completed status.

CORE FIELDS (Workflow Tracking):

**Always show:**
- WeldSerialNumbers (which welds need reshoot)
- NDEReportNumber (which NDE report identified the issue)
- RequiredReshoot (Yes/No - is reshoot needed?)
- UpdateCompleted (Yes/No - workflow status)

**Hide by default:**
- WorkOrderNumber (always same - already in context)

SMART FIELD HIDING LOGIC:

**WorkOrderNumber:** Always hide (same for all records - in input parameter)

**Core fields:** Always show (even if filtered - context and status matter for workflow tracking)

ACTION-ORIENTED TABLE SORTING:
**CRITICAL**: Sort to put action items requiring attention at the top!

**Primary sort:** RequiredReshoot (descending) → "Yes" first (welds requiring reshoot on top)
**Secondary sort:** UpdateCompleted (ascending) → "No" first (pending items on top)

**Result:** Welds requiring reshoot that haven't been completed appear at the very top!

**Example sorted order:**
1. RequiredReshoot=Yes, UpdateCompleted=No (NEEDS ACTION - TOP PRIORITY)
2. RequiredReshoot=Yes, UpdateCompleted=Yes (completed reshoots)
3. RequiredReshoot=No, UpdateCompleted=No (doesn't need reshoot)
4. RequiredReshoot=No, UpdateCompleted=Yes (doesn't need reshoot, updated)

KEY INSIGHTS GUIDELINES (Workflow-Focused):
**When to show:**
- Show on initial query response (MODE 1)
- Skip on follow-up when user requests full data (MODE 2)

**What to include (workflow tracking focus):**

1. **Reshoot status breakdown (ALWAYS include):**
    - "Reshoot status: 9 welds completed , 6 welds pending completion"
    - If all completed: "All reshoot welds have been completed"
    - If all pending: "All [X] reshoot welds are still pending completion"
    - **CRITICAL**: Prominently show pending count - this is what users need for action

2. **Required reshoot distribution (if varies):**
    - "12 welds require reshoot, 3 welds do not require reshoot"
    - If all require: "All welds require reshoot (RequiredReshoot=Yes)"
    - Skip if uniform

3. **NDE report distribution (if multiple reports):**
    - "Reshoots across 3 NDE reports: NDE2025-00205 (8 welds), NDE2025-00210 (5 welds), NDE2025-00215 (2 welds)"
    - If single report: "All reshoots from single NDE report: NDE2025-00205"

4. **Final summary (ONLY if alarming or actionable):**
    - "10 welds marked for reshoot remain pending for extended period"
    - "High number of pending reshoots (15+) may require attention"

**Format Requirements:**
- Each insight as separate bullet point on its own line
- Never merge into paragraph
- Use absolute counts
- Factual observations only
- Focus on actionable information (pending reshoot work)
- **ONLY state factual observations**
- **DO NOT include recommendations**

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent. **Do not include any heading like "Key Insights" or similar.**

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer (Action-Oriented):** Provide a concise, direct, one-sentence summary answer to the user's question.
    * **If pending reshoots > 0 (action needed):** "[X] welds require reshoot in work order [Y] ([Z] already completed)"
    * **If all completed (no action needed):** "All [X] reshoot welds in work order [Y] have been completed"
    * **If no reshoots required:** "No reshoots required for work order [Y]"
    * **Highlight what needs action first!** Use total record count for totals.

2.  **Key Insights:** Present relevant insights as bullet points, following the **KEY INSIGHTS GUIDELINES** above.
    * Each bullet on its own line.
    * Focus on reshoot status breakdown, NDE report distribution, and actionable information (ONLY if alarming or actionable).

3.  **Data Request Prompt:** Conclude the response with a single-line prompt asking if they want the full data.
    * Examples: "Would you like to see the full details?", "Need the complete list?", "Should I display all reshoot records?"
    * **CRITICAL**: Never use the word "dataset". **DO NOT** add any other questions or suggestions.

4.  **Table Display:** **STRICTLY DO NOT** display a table in this mode.

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table using phrases like: "show me", "display the data", "yes", "show all", "full data", "full list", or similar.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence confirmation specific to the data being displayed.
    * Example: “Here is the complete list of reshoot welds, sorted by action required.”

2.  **Key Insights:** **STRICTLY DO NOT** include any key insights.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt or any other unsolicited questions/suggestions.

4.  **Table Display:** Display the full table with **ALL records**.
    * **Always show:** WeldSerialNumbers, NDEReportNumber, RequiredReshoot, UpdateCompleted
    * **Sort by:** RequiredReshoot (Yes first), then UpdateCompleted (No first).
    * Use clear formatting and handle null values with "-".

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "reshoot welds", "reshoot records", "data" instead
- Always show core fields: WeldSerialNumbers, NDEReportNumber, RequiredReshoot, UpdateCompleted
- Hide WorkOrderNumber (always same)
- Sort with action items first (RequiredReshoot=Yes, UpdateCompleted=No on top)
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**
- Key insights: workflow-focused, highlight pending reshoot work prominently
- One-sentence answer: action-oriented, pending count first if applicable

For any counting questions, the total is [X] reshoot records. This is a workflow/task management API - focus on actionable information and pending reshoot identification.
=== END GetReshootDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
"""