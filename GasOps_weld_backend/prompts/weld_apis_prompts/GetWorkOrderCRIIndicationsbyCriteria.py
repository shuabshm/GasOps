def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWorkOrderCRIIndicationsbyCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetWorkOrderCRIIndicationsbyCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns CRI indication details with flexible grouping, showing counts of indications grouped by specified dimensions.

RESPONSE STRUCTURE:
The API returns grouped aggregation data with dynamic structure based on GroupBy parameter.

AVAILABLE FIELDS (Dynamic based on GroupBy):
- WorkOrderNumber: Work order identifier (can be filter or GroupBy field)
- WeldSerialNumber: Weld serial identifier (can be filter or GroupBy field)
- Indication: Type of CRI indication (e.g., Porosity, Slag Inclusions, Crack, Undercut, etc.)
- CRIName: CRI inspector name (can be filter or GroupBy field)
- WelderName: Welder name (can be filter parameter only)
- Count: Number of occurrences for the grouped combination

FIELD DISPLAY LOGIC:
**CRITICAL**: The response structure is DYNAMIC based on the GroupBy parameter.

**Always Show:**
- Indication column (always present in response)
- Count column

**Show GroupBy Column ONLY IF:**
- The GroupBy field is NOT used as a filter parameter in the payload
- Example: If GroupBy=["CRIName"] and CRIName is NOT in payload → Show CRIName column
- Example: If GroupBy=["WorkOrderNumber"] but WorkOrderNumber IS in payload → Hide WorkOrderNumber column

**Smart Field Hiding (Payload Filter Parameters):**
- **ALWAYS hide ANY field that appears in the payload as a filter parameter**, regardless of whether it's in GroupBy
- WorkOrderNumber: Hide if present in payload
- WeldSerialNumber: Hide if present in payload
- WelderName: Hide if present in payload
- CRIName: Hide if present in payload

**Rule**: If a field is in the payload (as a filter parameter) → ALWAYS hide it, even if it's the GroupBy field

**Display Examples:**
- Payload: `{"WorkOrderNumber": "100500514", "GroupBy": ["WorkOrderNumber"]}` → Columns: Indication, Count
- Payload: `{"WeldSerialNumber": "250129", "GroupBy": ["WeldSerialNumber"]}` → Columns: Indication, Count
- Payload: `{"WorkOrderNumber": "100500514", "GroupBy": ["CRIName"]}` → Columns: CRIName, Indication, Count
- Payload: `{"WorkOrderNumber": "100500514", "WelderName": "John", "GroupBy": ["WorkOrderNumber"]}` → Columns: Indication, Count

Field Display Rules:
- Use "-" for null/empty values
- Maintain column ordering: GroupBy fields first (if shown), then Indication, then Count
- Use clear column headers

TABLE SORTING:
**CRITICAL**: ALWAYS sort by Count descending (most frequent indications first)

TARGETED KEY INSIGHTS:
**Match insights focus to GroupBy pattern:**

| GroupBy Pattern | Insights Focus |
|----------------|----------------|
| ["WorkOrderNumber"] | Work order CRI indication analysis, most common indication types, quality patterns |
| ["WeldSerialNumber"] | Weld-level CRI indication analysis, specific weld quality issues |
| ["CRIName"] | Inspector patterns, CRI performance analysis, indication detection patterns per inspector |

**Always include:**
- Total grouped record count
- Most frequent indication types (top 1-3 with their counts)
- Comparison between different indication types
- If sample displayed, provide overall statistics for full dataset

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent. Do not include any headings, additional commentary, or explanations.

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence summary answer to the user's specific question from a business perspective.
    * Use total record count as the total count when reporting the volume.
    * Mention applied filters for context.
    * Examples:
        * "Work order 100500514 has 2 CRI indication types, with Porosity being the most frequent at 275 occurrences."
        * "Weld serial 250129 has 3 CRI indication types, with Slag Inclusions occurring 15 times."
        * "CRI inspector John Smith identified 4 indication types in work order 100500514."

2.  **Key Takeaways(Do Not include any heading like "Key Takeaways" or "Insights" or similar):** Provide targeted insights as separate bullet points following the **TARGETED KEY INSIGHTS** guidelines.
    * Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
    * Focus insights on CRI indication count distribution and comparison between different indication types.

3.  **Data Request Prompt:** Conclude the response with a single-line prompt asking if they want the full data.
    * Examples: "Would you like to see the detailed breakdown?", "Need the complete data?", "Should I display all grouped records?"
    * **CRITICAL**: Never use the word "dataset". **DO NOT** add any other questions or suggestions.

4.  **Table Display:** **STRICTLY DO NOT** display any table in this mode.

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table using phrases like: "show me", "display the data", "yes", "show all", "full data", "full list", or similar.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence confirmation specific to the data being displayed.
    * Example: "Here is the full table of CRI indications for work order 100500514, sorted by frequency."

2.  **Key Takeaways:** **STRICTLY DO NOT** include any key takeaways.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt or any other unsolicited questions/suggestions.

4.  **Table Display:** Display the full table with **ALL rows**.
    * **ALWAYS show**: Indication column and Count column
    * **Show GroupBy column ONLY IF it's NOT in the payload as a filter parameter**
    * **ALWAYS hide ANY field that appears in the payload** (WorkOrderNumber, WeldSerialNumber, WelderName, CRIName)
    * **Sort by Count descending** (most frequent first).
    * Use clear formatting and handle null values with "-".

**Display Examples based on Payload:**
- Payload: `{"WorkOrderNumber": "100500514", "GroupBy": ["WorkOrderNumber"]}` → Columns: Indication, Count
- Payload: `{"WeldSerialNumber": "250129", "GroupBy": ["WeldSerialNumber"]}` → Columns: Indication, Count
- Payload: `{"WorkOrderNumber": "100500514", "GroupBy": ["CRIName"]}` → Columns: CRIName, Indication, Count

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "grouped records", "records", "data" instead
- **Initial Response (MODE 1): NO TABLE** - just answer + key takeaways + data request prompt
- **Follow-up Response (MODE 2): FULL TABLE with ALL rows** - no key takeaways
- Fields to display: **ONLY show Indication + Count. Show GroupBy column ONLY IF it's NOT in payload**
- Filter fields: **ALWAYS HIDE any field present in the payload**, regardless of GroupBy
- Sorting: ALWAYS Count descending (most frequent first)
- Key insights: Focus on CRI indication distribution and comparison between indication types
- One-sentence answer: Mention applied filters for context
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**
- Always use absolute numbers for counts not percentages

For any counting questions, the total is [X] grouped records. Focus on providing targeted analysis based on the grouping dimensions, with emphasis on CRI indication distribution patterns and comparing different indication types.
=== END GetWorkOrderCRIIndicationsbyCriteria GUIDELINES ===
"""
