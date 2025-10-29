def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWorkOrderRejactableCRIIndicationsbyCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetWorkOrderRejactableCRIIndicationsbyCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns **rejectable** CRI indication details with flexible grouping, showing counts of critical quality defects that require attention.

**CRITICAL CONTEXT**: This API focuses ONLY on **rejectable** indications (quality defects requiring action/repair), not all indications.

RESPONSE STRUCTURE:
The API returns grouped aggregation data with dynamic structure based on GroupBy parameter.

AVAILABLE FIELDS (Dynamic based on GroupBy):
- WorkOrderNumber: Work order identifier (can be filter or GroupBy field)
- WeldSerialNumber: Weld serial identifier (can be filter or GroupBy field)
- Indication: Type of rejectable CRI indication (e.g., Burn Through, Porosity, Slag Inclusions, Crack, etc.)
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
- Payload: `{"WeldSerialNumber": "240911", "GroupBy": ["WeldSerialNumber"]}` → Columns: Indication, Count
- Payload: `{"WorkOrderNumber": "100500514", "GroupBy": ["CRIName"]}` → Columns: CRIName, Indication, Count
- Payload: `{"WorkOrderNumber": "100500514", "WelderName": "John", "GroupBy": ["WorkOrderNumber"]}` → Columns: Indication, Count

Field Display Rules:
- Use "-" for null/empty values
- Maintain column ordering: GroupBy fields first (if shown), then Indication, then Count
- Use clear column headers

TABLE SORTING:
**CRITICAL**: ALWAYS sort by Count descending (most critical rejectable indications first)

TARGETED KEY INSIGHTS:
**Match insights focus to GroupBy pattern with QUALITY EMPHASIS:**

| GroupBy Pattern | Insights Focus |
|----------------|----------------|
| ["WorkOrderNumber"] | Work order rejectable CRI indication analysis, most critical defect types, quality concern areas |
| ["WeldSerialNumber"] | Weld-level critical defects, specific welds needing repair/attention |
| ["CRIName"] | Inspector detection patterns for rejectable defects, rejection consistency |

**Always include:**
- Total grouped record count
- Most critical/frequent rejectable indication (top 1-3)
- **Quality emphasis**: Highlight areas needing attention, repair requirements
- If sample displayed, provide overall statistics for full dataset

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent. Do not include any headings, additional commentary, or explanations.

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence summary answer to the user's specific question from a business perspective.
    * Use total record count as the total count when reporting the volume.
    * Mention applied filters for context.
    * **Emphasize quality/rejection aspect** when appropriate.
    * Examples:
        * "Work order 100500514 has 3 rejectable CRI indication types, with Burn Through being the most critical at 15 occurrences."
        * "Weld serial 240911 has 2 rejectable CRI defect types, requiring immediate attention."
        * "CRI inspector John Smith identified 4 rejectable indication types requiring repair action."

2.  **Key Takeaways(Do not include any heading like "Key Takeaways" or "Insights" or similar):** Provide targeted insights as separate bullet points following the **TARGETED KEY INSIGHTS** guidelines.
    * Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
    * **Focus insights on what's in the GroupBy with QUALITY EMPHASIS** (these are rejectable defects requiring action).
    * Highlight the most frequent/critical rejectable indications and their counts.
    * **Emphasize areas needing attention, repair requirements, quality improvement opportunities**

3.  **Data Request Prompt:** Conclude the response with a single-line prompt asking if they want the full data.
    * Examples: "Would you like to see the detailed breakdown?", "Need all grouped records?", "Should I display the complete data?"
    * **CRITICAL**: Never use the word "dataset". **DO NOT** add any other questions or suggestions.

4.  **Table Display:** **STRICTLY DO NOT** display any table in this mode.

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table using phrases like: "show me", "display the data", "yes", "show all", "full data", "full list", or similar.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence confirmation specific to the data being displayed.
    * Example: "Here is the full table of rejectable CRI indications for work order 100500514, sorted by criticality/frequency."

2.  **Key Takeaways:** **STRICTLY DO NOT** include any key takeaways.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt or any other unsolicited questions/suggestions.

4.  **Table Display:** Display the full table with **ALL rows**.
    * **ALWAYS show**: Indication column and Count column
    * **Show GroupBy column ONLY IF it's NOT in the payload as a filter parameter**
    * **ALWAYS hide ANY field that appears in the payload** (WorkOrderNumber, WeldSerialNumber, WelderName, CRIName)
    * **Sort by Count descending** (most critical rejectable indications first).
    * Use clear formatting and handle null values with "-".

**Display Examples based on Payload:**
- Payload: `{"WorkOrderNumber": "100500514", "GroupBy": ["WorkOrderNumber"]}` → Columns: Indication, Count
- Payload: `{"WeldSerialNumber": "240911", "GroupBy": ["WeldSerialNumber"]}` → Columns: Indication, Count
- Payload: `{"WorkOrderNumber": "100500514", "GroupBy": ["CRIName"]}` → Columns: CRIName, Indication, Count

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "grouped records", "records", "data" instead
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**
- **Always use absolute numbers for counts not percentages**
- Fields to display: **ONLY show Indication + Count. Show GroupBy column ONLY IF it's NOT in payload**
- Filter fields: **ALWAYS HIDE any field present in the payload**, regardless of GroupBy
- Sorting: ALWAYS Count descending (most critical rejectable indications first)
- Key insights: TARGET to match GroupBy pattern with **QUALITY/ACTION** emphasis
- One-sentence answer: Mention applied filters and **emphasize quality/rejection aspect**
- **REMEMBER**: These are REJECTABLE indications requiring action - emphasize quality concerns

For any counting questions, the total is [X] grouped records. Focus on providing targeted analysis based on the grouping dimensions, with emphasis on rejectable CRI indication distribution, quality concerns, and areas requiring attention/repair.
=== END GetWorkOrderRejactableCRIIndicationsbyCriteria GUIDELINES ===
"""
