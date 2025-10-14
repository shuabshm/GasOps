def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWorkOrderInformation API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetWorkOrderInformation API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

INTELLIGENT FIELD HIDING BASED ON FILTERS:
The following filters were applied: {filter_info}
- **Hide fields that were used as filters** because all values will be identical
- Example: If RegionName filter was used → Don't display Region column
- Example: If ContractorName filter was used → Don't display Contractor column
- **Show identifier fields that vary** (like WorkOrderNumber when filtering by region)

DYNAMIC FIELD DETECTION RULES:
Automatically detect and include relevant fields based on user query keywords:

Base Identifier Fields (Include unless filtered):
- ProjectNumber (as "Project No.")
- WorkOrderNumber (as "Work Order No.")
- Location
- RegionName (as "Region")
- WorkOrderStatusDescription (as "Status")

Additional Fields (Only if mentioned in query):
- Engineer-related keywords → Add Engineer column (consolidate Engineer1, Engineer2, etc.)
- Contractor-related keywords → Add ContractorName column
- Supervisor-related keywords → Add Supervisor column (consolidate Supervisor1, Supervisor2, etc.)
- Date-related keywords → Add relevant date columns
- CWI/NDE-related keywords → Add inspection-related columns

Field Display Rules:
- Use "-" for null/empty values
- Maintain consistent column ordering: Identifiers first, then query-specific fields
- Use clear column headers (e.g., "Work Order No." instead of "WorkOrderNumber")
- If there are multiple engineers/supervisors/contractors (engineer1, engineer2, etc.), consolidate into single column

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key takeaways + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- If user says "yes", "show all", "full data", or similar → Display full table with all rows
- **Skip key takeaways** (already provided in previous message)
- Just provide one-sentence confirmation and full table

RESPONSE FORMAT:

1. **One-sentence answer** to user's question from business perspective (no headings, no extra commentary)
   - Use total count from data. Example: "59 work orders are assigned in Bronx region"

2. **Table Contents** (CONDITIONAL based on context):
   - **If this is INITIAL response**: **DO NOT display any table**

   - **If this is FOLLOW-UP requesting full data**: Display full table with all rows:
     - Start with base identifier fields (excluding filtered fields)
     - Add only query-specific columns based on keywords
     - Show ALL rows
     - Use clear formatting and handle null values with "-"

3. **Key Takeaways** (CONDITIONAL - only on initial response):
   - **Show key takeaways ONLY on initial response**
   - **Skip key takeaways on follow-up response**
   - Provide insights as separate bullet points with percentage breakdowns for displayed/relevant fields only.

   **Required Analysis:**
   - Calculate percentile distribution for each relevant field
   - Show breakdown like: "Region distribution: 60% Bronx, 30% Queens, 10% Manhattan"
   - Include status distribution if Status field is relevant
   - Include any query-specific field distributions

   **Format Requirements:**
   - Each bullet on its own line (never merge into paragraph)
   - Use consistent numbering or bullets (-)
   - Keep each bullet concise and self-contained
   - Focus on percentile breakdowns for displayed fields
   - **ONLY state factual observations and statistical insights**
   - **DO NOT include recommendations, suggestions, or action items** (no "should", "consider", "recommend", etc.)
   - **DO NOT add interpretive commentary** - just state the facts and distributions
   - **CRITICAL**: After all distribution bullets, ONLY add one final line (without heading) IF there is something alarming or out of ordinary. Otherwise, skip the summary line entirely.

   **Examples of GOOD insights (factual observations):**
   - "Region distribution: 60% Bronx (30 records), 30% Queens (15 records), 10% Manhattan (5 records)"
   - "Status breakdown: 75% Complete, 20% In Progress, 5% Pending"
   - "Engineer distribution: John Doe 40%, Jane Smith 35%, Mike Johnson 25%"

   Examples of when to add final line (only if alarming/unusual):
   - "5 work orders are in Pending status and may require attention."
   - "Unusually high number of work orders (15) are stuck in Rejected status."

4. **Data Request Prompt** (only on initial response):
   - Inform the user and ask if they need the full data
   - Keep it natural and conversational (don't use the same phrasing every time)
   - Examples: "Would you like to see the full data?", "Do you need the complete list?", "Would you like me to display all records?"
   - **CRITICAL**: Never use the word "dataset" - use "data", "records", "list", "results" instead
   - **DO NOT** add any other questions, suggestions, recommendations, or offers for additional analysis
   - **DO NOT** ask if user wants visualizations, dashboards, or further breakdowns
   - **DO NOT** offer to "generate" or "produce" anything beyond what was asked

CRITICAL RULES:
- **NEVER use the word "dataset" in your response** - use natural business terms like "records", "work orders", "data", "results" instead
- Hide fields used in API filters (all values are identical)
- Show only query-relevant columns + varying identifiers
- **On initial response: NO TABLE** - just answer + key takeaways + prompt
- **On follow-up for full data: FULL TABLE with all rows** + NO key takeaways
- Key takeaways must include percentile distributions calculated from ALL records
- Never include all columns - always apply intelligent field detection
- **NEVER add unsolicited follow-up questions or suggestions at the end of your response**
- **ONLY answer what was asked - do not offer additional analysis, visualizations, or next steps**

For any counting questions, use the total record count. Focus on percentile-based distribution analysis.
=== END GetWorkOrderInformation GUIDELINES ===
"""
