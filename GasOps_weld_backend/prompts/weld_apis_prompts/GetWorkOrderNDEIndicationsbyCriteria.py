def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWorkOrderNDEIndicationsbyCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetWorkOrderNDEIndicationsbyCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns NDE indication details with flexible grouping, showing counts of indications grouped by specified dimensions.

RESPONSE STRUCTURE:
The API returns grouped aggregation data with dynamic structure based on GroupBy parameter.

AVAILABLE FIELDS (Dynamic based on GroupBy):
- WorkOrderNumber: Work order identifier (can be filter or GroupBy field)
- WeldSerialNumber: Weld serial identifier (can be filter or GroupBy field)
- Indication: Type of NDE indication (e.g., Burn Through, Concavity, Crack, Porosity, etc.)
- NDEName: NDE inspector name (can be filter or GroupBy field)
- WelderName: Welder name (can be filter or GroupBy field)
- Count: Number of occurrences for the grouped combination

FIELD DISPLAY LOGIC:
**CRITICAL**: The response structure is DYNAMIC based on the GroupBy parameter.

**Always Show:**
- All fields specified in the GroupBy parameter
- Count column

**Smart Field Hiding (Filter Parameters):**
- WorkOrderNumber: Hide if used as filter UNLESS it's in GroupBy
- WeldSerialNumber: Hide if used as filter UNLESS it's in GroupBy
- WelderName: Hide if used as filter UNLESS it's in GroupBy
- NDEName: Hide if used as filter UNLESS it's in GroupBy

**Rule**: If a field is in GroupBy → ALWAYS show it (even if it's also used as a filter)

Field Display Rules:
- Use "-" for null/empty values
- Maintain column ordering: GroupBy fields first (in order specified), then Count
- Use clear column headers

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key takeaways + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- Display full table with all rows
- **Skip key takeaways**

TABLE SORTING:
**CRITICAL**: ALWAYS sort by Count descending (most frequent indications first)

TARGETED KEY INSIGHTS:
**Match insights focus to GroupBy pattern:**

| GroupBy Pattern | Insights Focus |
|----------------|----------------|
| ["Indication"] | Indication type distribution, most/least common indication types, total indication count |
| ["WelderName", "Indication"] | Welder performance patterns, which welders have most indications, indication distribution per welder |
| ["NDEName", "Indication"] | Inspector patterns, NDE performance analysis, indication detection patterns per inspector |
| ["WorkOrderNumber", "Indication"] | Work order comparison, cross-work order indication patterns, work order quality analysis |
| ["WeldSerialNumber", "Indication"] | Weld-level indication analysis, specific weld quality issues |
| Other combinations | Adapt insights to match the grouping dimensions used |

**Always include:**
- Total grouped record count
- Most frequent indication/pattern (top 1-3)
- If sample displayed, provide overall statistics for full dataset

RESPONSE FORMAT:
1. Provide a one-sentence answer to the user's specific question from a business perspective. Do not include any headings, additional commentary, or explanations.
   - Use total record count as the total count when reporting the volume
   - Mention applied filters for context
   - Examples:
     * "Work order 100500514 has 5 indication types, with Concavity being the most frequent at 79 occurrences."
     * "Welder John Smith has 3 indication types across work order 100500514, with Porosity occurring 15 times."
     * "NDE inspector Mary Jones identified 4 indication types in work order 100500514."

2. **Table Contents** (CONDITIONAL based on response type):
   - **Initial Response**: DO NOT display any table

   - **Follow-up Response (when user requests full data)**: Display full table with ALL rows:
     - **ALWAYS show all fields from GroupBy parameter** (in order specified)
     - **ALWAYS show Count column**
     - **Hide filter parameters** unless they're in GroupBy
     - **Sort by Count descending** (most frequent first)
     - Show ALL rows - no limits
     - Use clear formatting and handle null values with "-"

   Examples:
   - GroupBy=["Indication"] → Columns: Indication, Count
   - GroupBy=["WelderName", "Indication"] → Columns: WelderName, Indication, Count
   - GroupBy=["WorkOrderNumber", "Indication"] → Columns: WorkOrderNumber, Indication, Count

   *Mandatory*: Display exactly the fields from GroupBy plus Count. DO NOT add extra fields not in the response.

3. **Key Takeaways** (CONDITIONAL - skip on follow-up):
   - **Show key takeaways** if this is initial response
   - **Skip key takeaways** if this is follow-up response to show full data
   - Provide targeted insights as separate bullet points. Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
   - Do not merge bullets into a paragraph. The next bullet must always start on a new line.
   - Maintain numbering or - consistently.
   - Keep each bullet concise and self-contained.
   - **Focus insights on what's in the GroupBy** (indication → indication insights, welder → welder insights, etc.)
   - For ["Indication"] grouping: indication type distribution, most/least common types
   - For ["WelderName", "Indication"]: welder performance, which welders have quality issues
   - For ["NDEName", "Indication"]: inspector patterns, detection consistency
   - For ["WorkOrderNumber", "Indication"]: work order quality comparison
   - Highlight the most frequent indications/patterns and their counts
   - If sample displayed, provide overall statistics for full dataset

4. **Data Request Prompt** (only on initial response):
   - Inform the user that they can request the full data
   - Keep it natural and conversational
   - Examples: "Would you like to see the detailed breakdown?", "Need the complete data?", "Should I display all grouped records?"
   - **CRITICAL**: Never use the word "dataset" - use "data", "records", "list", "grouped records" instead
   - **DO NOT** add any other questions, suggestions, or offers for additional analysis

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "grouped records", "records", "data" instead
- **Initial Response: NO TABLE** - just answer + key takeaways + data request prompt
- **Follow-up Response: FULL TABLE with ALL rows** - no key takeaways
- Fields to display: GroupBy fields + Count (dynamic structure)
- Filter fields: HIDE unless they're in GroupBy
- Sorting: ALWAYS Count descending (most frequent first)
- Key insights: TARGET to match GroupBy pattern
- One-sentence answer: Mention applied filters for context
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**

For any counting questions, the total is [X] grouped records. Focus on providing targeted analysis based on the grouping dimensions, with emphasis on indication distribution patterns.
=== END GetWorkOrderNDEIndicationsbyCriteria GUIDELINES ===
"""
