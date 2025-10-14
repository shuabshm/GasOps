def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWorkOrderRejactableNDEIndicationsbyCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetWorkOrderRejactableNDEIndicationsbyCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns **rejectable** NDE indication details with flexible grouping, showing counts of critical quality defects that require attention.

**CRITICAL CONTEXT**: This API focuses ONLY on **rejectable** indications (quality defects requiring action/repair), not all indications.

RESPONSE STRUCTURE:
The API returns grouped aggregation data with dynamic structure based on GroupBy parameter.

AVAILABLE FIELDS (Dynamic based on GroupBy):
- WorkOrderNumber: Work order identifier (can be filter or GroupBy field)
- WeldSerialNumber: Weld serial identifier (can be filter or GroupBy field)
- Indication: Type of rejectable NDE indication (e.g., Porosity, Lack of Fusion, Crack, Incomplete Penetration, etc.)
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
**CRITICAL**: ALWAYS sort by Count descending (most critical rejectable indications first)

TARGETED KEY INSIGHTS:
**Match insights focus to GroupBy pattern with QUALITY EMPHASIS:**

| GroupBy Pattern | Insights Focus |
|----------------|----------------|
| ["Indication"] | Rejectable indication type distribution, most critical defect types, quality concern areas |
| ["WelderName", "Indication"] | Welder quality issues, which welders have most rejectable defects, training/attention needs |
| ["NDEName", "Indication"] | Inspector detection patterns for rejectable defects, rejection consistency |
| ["WorkOrderNumber", "Indication"] | Work order quality comparison, cross-work order rejection patterns, quality trends |
| ["WeldSerialNumber", "Indication"] | Weld-level critical defects, specific welds needing repair/attention |
| Other combinations | Adapt insights to match the grouping dimensions used |

**Always include:**
- Total grouped record count
- Most critical/frequent rejectable indication (top 1-3)
- **Quality emphasis**: Highlight areas needing attention, repair requirements
- If sample displayed, provide overall statistics for full dataset

RESPONSE FORMAT:
1. Provide a one-sentence answer to the user's specific question from a business perspective. Do not include any headings, additional commentary, or explanations.
   - Use total record count as the total count when reporting the volume
   - Mention applied filters for context
   - **Emphasize quality/rejection aspect** when appropriate
   - Examples:
     * "Work order 101351590 has 3 rejectable indication types, with Porosity being the most critical at 4 occurrences."
     * "Welder John Smith has 2 rejectable defect types in work order 100500514, requiring immediate attention."
     * "NDE inspector Mary Jones identified 5 rejectable indication types requiring repair action."

2. **Table Contents** (CONDITIONAL based on response type):
   - **Initial Response**: DO NOT display any table

   - **Follow-up Response (when user requests full data)**: Display full table with ALL rows:
     - **ALWAYS show all fields from GroupBy parameter** (in order specified)
     - **ALWAYS show Count column**
     - **Hide filter parameters** unless they're in GroupBy
     - **Sort by Count descending** (most critical/frequent rejectable indications first)
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
   - **Focus insights on what's in the GroupBy with QUALITY EMPHASIS** (these are rejectable defects requiring action)
   - For ["Indication"] grouping: rejectable indication distribution, most critical defect types, quality concerns
   - For ["WelderName", "Indication"]: welder quality performance, who needs training/attention, defect patterns per welder
   - For ["NDEName", "Indication"]: inspector rejection patterns, detection consistency for critical defects
   - For ["WorkOrderNumber", "Indication"]: work order quality issues, which work orders have quality concerns
   - Highlight the most frequent/critical rejectable indications and their counts
   - **Emphasize areas needing attention, repair requirements, quality improvement opportunities**
   - If sample displayed, provide overall statistics for full dataset

4. **Data Request Prompt** (only on initial response):
   - Inform the user that they can request the full data
   - Keep it natural and conversational
   - Examples: "Would you like to see the detailed breakdown?", "Need all grouped records?", "Should I display the complete data?"
   - **CRITICAL**: Never use the word "dataset" - use "grouped records", "data", "records", "list" instead
   - **DO NOT** add any other questions, suggestions, or offers for additional analysis

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "grouped records", "records", "data" instead
- **Initial Response: NO TABLE** - just answer + key takeaways + data request prompt
- **Follow-up Response: FULL TABLE with ALL rows** - no key takeaways
- Fields to display: GroupBy fields + Count (dynamic structure)
- Filter fields: HIDE unless they're in GroupBy
- Sorting: ALWAYS Count descending (most critical rejectable indications first)
- Key insights: TARGET to match GroupBy pattern with QUALITY/ACTION emphasis
- One-sentence answer: Mention applied filters and emphasize quality/rejection aspect
- **REMEMBER**: These are REJECTABLE indications requiring action - emphasize quality concerns
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**

For any counting questions, the total is [X] grouped records. Focus on providing targeted analysis based on the grouping dimensions, with emphasis on rejectable indication distribution, quality concerns, and areas requiring attention/repair.
=== END GetWorkOrderRejactableNDEIndicationsbyCriteria GUIDELINES ===
"""
