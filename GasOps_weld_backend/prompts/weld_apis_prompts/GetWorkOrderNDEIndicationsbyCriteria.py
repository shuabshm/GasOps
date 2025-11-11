# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetWorkOrderNDEIndicationsbyCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     filter_info = api_parameters if api_parameters else {}

#     return f"""
# === GetWorkOrderNDEIndicationsbyCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API returns NDE indication details with flexible grouping, showing counts of indications grouped by specified dimensions.

# RESPONSE STRUCTURE:
# The API returns grouped aggregation data with dynamic structure based on GroupBy parameter.

# AVAILABLE FIELDS (Dynamic based on GroupBy):
# - WorkOrderNumber: Work order identifier (can be filter or GroupBy field)
# - WeldSerialNumber: Weld serial identifier (can be filter or GroupBy field)
# - Indication: Type of NDE indication (e.g., Burn Through, Concavity, Crack, Porosity, etc.)
# - NDEName: NDE inspector name (can be filter or GroupBy field)
# - WelderName: Welder name (can be filter or GroupBy field)
# - Count: Number of occurrences for the grouped combination

# FIELD DISPLAY LOGIC:
# **CRITICAL**: The response structure is DYNAMIC based on the GroupBy parameter.

# **Always Show:**
# - All fields specified in the GroupBy parameter
# - Count column

# **Smart Field Hiding (Filter Parameters):**
# - WorkOrderNumber: Hide if used as filter UNLESS it's in GroupBy
# - WeldSerialNumber: Hide if used as filter UNLESS it's in GroupBy
# - WelderName: Hide if used as filter UNLESS it's in GroupBy
# - NDEName: Hide if used as filter UNLESS it's in GroupBy

# **Rule**: If a field is in GroupBy → ALWAYS show it (even if it's also used as a filter)

# Field Display Rules:
# - Use "-" for null/empty values
# - Maintain column ordering: GroupBy fields first (in order specified), then Count
# - Use clear column headers

# **SINGLE STABLE RESPONSE - NO FOLLOW-UP QUESTIONS**

# Provide a complete, one-time response with NO follow-up questions or prompts. The response must be self-contained and complete.

# **FORMAT VARIES BY GroupBy PARAMETER:**

# **CASE 1: GroupBy = ["WelderName"] (Group by Welder)**

# 1. **Opening Statement:**
#    "Got it — now that we're grouping by welder instead of indication type, we do have results for work order [WorkOrderNumber]."

# 2. **Context Line:**
#    "Here's the breakdown of NDE indications by welder, with total counts and the types of indications each welder had:"

# 3. **Table Display:**
#    Display a 3-column table:

#    | Welder | Indication Types & Counts | Total Indications |
#    |--------|--------------------------|-------------------|
#    | [Welder Name 1] | [Indication1] (count), [Indication2] (count), [Indication3] (count) | [Total] |
#    | [Welder Name 2] | [Indication1] (count), [Indication2] (count) | [Total] |

#    **Table Rules:**
#    - Sort by Total Indications descending (highest first)
#    - Middle column: List all indication types with counts in format "Indication (count), Indication (count)"
#    - Show ALL welders (no row limits)
#    - Use clear formatting and handle null values with "-"

# 4. **Key Insights(**DO NOT use headers like "Key Takeaways", "Key Insights", "Insights", etc.**.):**
#    - Provide 3-4 bullet points (use • bullets)
#    - Focus on welder performance patterns
#    - Highlight which welders have most indications
#    - Identify most frequent indication types per welder
#    - Note any patterns or trends

# 5. **NO FOLLOW-UP QUESTIONS** - End after Key Insights

# **CASE 2: GroupBy = ["WeldSerialNumber"] (Group by Weld Serial Number)**

# 1. **Opening Statement:**
#    "Got it — now that we're grouping by weld serial number instead of indication type, we do have results for work order [WorkOrderNumber]."

# 2. **Context Line:**
#    "Here's the breakdown of NDE indications by weld serial number, with total counts and the types of indications each weld had:"

# 3. **Table Display:**
#    Display a 3-column table:

#    | Weld Serial Number | Indication Types & Counts | Total Indications |
#    |-------------------|--------------------------|-------------------|
#    | [WeldSerial1] | [Indication1] (count), [Indication2] (count) | [Total] |
#    | [WeldSerial2] | [Indication1] (count) | [Total] |

#    **Table Rules:**
#    - Sort by Total Indications descending (highest first)
#    - Middle column: List all indication types with counts in format "Indication (count), Indication (count)"
#    - Show ALL weld serial numbers (no row limits)
#    - Use clear formatting and handle null values with "-"

# 4. **Key Insights(**DO NOT use headers like "Key Takeaways", "Key Insights", "Insights", etc.**.):**
#    - Provide 3-4 bullet points (use • bullets)
#    - Focus on weld-level indication analysis
#    - Highlight which welds have most quality issues
#    - Identify indication patterns per weld
#    - Note any critical welds requiring attention

# 5. **NO FOLLOW-UP QUESTIONS** - End after Key Insights

# **CASE 3: GroupBy = ["NDEName"] (Group by NDE Inspector)**

# 1. **Opening Statement:**
#    "Got it — now that we're grouping by NDE inspector instead of indication type, we do have results for work order [WorkOrderNumber]."

# 2. **Context Line:**
#    "Here's the breakdown of NDE indications by NDE inspector, with total counts and the types of indications each inspector identified:"

# 3. **Table Display:**
#    Display a 3-column table:

#    | NDE Inspector | Indication Types & Counts | Total Indications |
#    |--------------|--------------------------|-------------------|
#    | [Inspector1] | [Indication1] (count), [Indication2] (count) | [Total] |
#    | [Inspector2] | [Indication1] (count) | [Total] |

#    **Table Rules:**
#    - Sort by Total Indications descending (highest first)
#    - Middle column: List all indication types with counts in format "Indication (count), Indication (count)"
#    - Show ALL NDE inspectors (no row limits)
#    - Use clear formatting and handle null values with "-"

# 4. **Key Insights(**DO NOT use headers like "Key Takeaways", "Key Insights", "Insights", etc.**.):**
#    - Provide 3-4 bullet points (use • bullets)
#    - Focus on inspector detection patterns
#    - Highlight which inspectors identified most indications
#    - Compare indication detection consistency
#    - Note any inspector-specific trends

# 5. **NO FOLLOW-UP QUESTIONS** - End after Key Insights

# **CASE 4: GroupBy = ["WorkOrderNumber"] (Group by Work Order) - SIMPLE FORMAT**

# 1. **Opening Statement:**
#    "Here are the NDE indications for work order [WorkOrderNumber]."

# 2. **Table Display:**
#    Display a simple 2-column table:

#    | Indication Type | Count |
#    |----------------|-------|
#    | [Indication1] | [count] |
#    | [Indication2] | [count] |

#    **Table Rules:**
#    - Sort by Count descending (highest first)
#    - Show ALL indication types (no row limits)
#    - Simple 2-column format (NO "Indication Types & Counts" column, NO "Total Indications" column)
#    - Use clear formatting and handle null values with "-"

# 3. **Key Insights(**DO NOT use headers like "Key Takeaways", "Key Insights", "Insights", etc.**.):**
#    - Provide 3-4 bullet points (use • bullets)
#    - Focus on indication type distribution
#    - Highlight most frequent indication types
#    - Note work order quality patterns
#    - Compare indication frequencies

# 4. **NO FOLLOW-UP QUESTIONS** - End after Key Insights

# **CASE 5: Other GroupBy Combinations**

# Follow the 3-column format pattern using the GroupBy field as the first column header, with "Indication Types & Counts" as middle column and "Total Indications" as third column.

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "grouped records", "records", "data" instead
# - **ALWAYS display table immediately** - no initial response without table
# - **ALWAYS include Key Insights** after the table(**DO NOT use headers like "Key Takeaways", "Key Insights", "Insights", etc.**.)
# - **NO FOLLOW-UP QUESTIONS** - end after Key Insights
# - Format varies by GroupBy: 3-column for entity grouping, 2-column for WorkOrderNumber
# - Sort by Total Indications (or Count) descending
# - Show ALL rows - no limits
# - **ONLY answer what was asked**

# For any counting questions, the total is [X] grouped records. Focus on providing targeted analysis based on the grouping dimensions, with emphasis on indication distribution patterns.
# === END GetWorkOrderNDEIndicationsbyCriteria GUIDELINES ===
# """



def get_api_prompt(api_parameters=None):
    """
    Returns the optimized API-specific prompt for GetWorkOrderNDEIndicationsbyCriteria API.
    
    Args:
        api_parameters (dict): Optional dictionary of API filter parameters
        
    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}
    
    return f"""
=== GetWorkOrderNDEIndicationsbyCriteria API - OPTIMIZED GUIDELINES ===
**CRITICAL GLOBAL RULES (APPLY TO ALL CASES):**
* **NEVER USE HEADERS FOR INSIGHTS:** Immediately after the table, provide Key Insights as a simple bulleted list. **DO NOT** use any headers (e.g., "Key Takeaways," "Key Insights," "Insights," "Analysis," etc.).
* **SINGLE STABLE RESPONSE:** Provide a complete, one-time response. **NO** follow-up questions or prompts. The response ends after the Key Insights.
* **Data Terminology:** **NEVER** use the word "dataset." Use "grouped records," "records," or "data."
* **Table Display:** **ALWAYS** display the table immediately after the Opening/Context lines. Show ALL rows (no row limits).
* **Sorting:** Tables must be sorted by the main count column ("Total Indications") descending (highest first) before displaying the table.
* **Null Values:** Use "-" for null/empty values.

---

**API OVERVIEW & FIELDS:**
This API returns NDE indication details, showing counts grouped by specified dimensions.

AVAILABLE FIELDS:
- WorkOrderNumber, WeldSerialNumber, Indication, NDEName, WelderName, Count (Count is the aggregation result).

**FIELD DISPLAY LOGIC:**
The response structure is DYNAMIC based on the GroupBy parameter.
1.  **Always Show:** All fields specified in the GroupBy parameter + Count column.
2.  **Ordering:** GroupBy fields first (in the order specified), then Count.
3.  **Smart Hiding:** A field used *only* as a filter (and not in GroupBy) must be hidden. If a field is in GroupBy, **ALWAYS** show it.

---

**RESPONSE FORMATS BY GroupBy PARAMETER:**

**COMMON TABLE RULES (For GroupBy != ["WorkOrderNumber"]):**
* **3-Column Format:** [GroupBy Field] | Indication Types & Counts | Total Indications
* **Middle Column:** List all indication types with counts: "Indication (count), Indication (count), ..."

**CASE 1: GroupBy = ["WelderName"] (Group by Welder)**
1.  **Opening/Context:** "Got it — here is the breakdown of NDE indications by welder for work order [WorkOrderNumber], showing total counts and the types of indications each welder had:"
2.  **Table:** 3-column format.
3.  **Key Insights (3-4 bullets):** Focus on welder performance patterns, identifying high-indication welders, most frequent indication types *per welder*, and trends.

**CASE 2: GroupBy = ["WeldSerialNumber"] (Group by Weld Serial Number)**
1.  **Opening/Context:** "Got it — here is the breakdown of NDE indications by weld serial number for work order [WorkOrderNumber], showing total counts and the types of indications each weld had:"
2.  **Table:** 3-column format.
3.  **Key Insights (3-4 bullets):** Focus on weld-level quality, highlighting high-issue welds, indication patterns *per weld*, and critical welds needing attention.

**CASE 3: GroupBy = ["NDEName"] (Group by NDE Inspector)**
1.  **Opening/Context:** "Got it — here is the breakdown of NDE indications by NDE inspector for work order [WorkOrderNumber], showing total counts and the types of indications each inspector identified:"
2.  **Table:** 3-column format.
3.  **Key Insights (3-4 bullets):** Focus on inspector detection patterns, highlighting inspectors who identified the most indications, consistency comparisons, and inspector-specific trends.

**CASE 4: GroupBy = ["WorkOrderNumber"] (Group by Work Order) - SIMPLE FORMAT**
1.  **Opening/Context:** "Here are the NDE indications for work order [WorkOrderNumber] aggregated by type."
2.  **Table:** Simple 2-column format: | Indication Type | Count |.
3.  **Key Insights (3-4 bullets):** Focus on indication type distribution, highlighting most frequent types, work order quality patterns, and frequency comparisons.

**CASE 5: Other GroupBy Combinations**
Follow the **COMMON TABLE RULES** (3-column format). The first column header is the GroupBy field name(s). Key Insights should provide targeted analysis based on the specific grouping dimensions.

---

**FINAL ACTION:** For any counting questions, state the total as "[X] grouped records." Focus on providing targeted analysis based on the grouping dimensions, with emphasis on indication distribution patterns.
=== END GetWorkOrderNDEIndicationsbyCriteria GUIDELINES ===
"""