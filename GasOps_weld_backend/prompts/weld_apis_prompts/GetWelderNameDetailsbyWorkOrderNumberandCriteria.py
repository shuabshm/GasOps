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

AVAILABLE FIELDS (Raw Data):
- WorkOrderNumber: Work order identifier
- WeldCategory: Category of weld (Production, Repaired, CutOut)
- WeldSerialNumber: Unique weld identifier
- Welder1, Welder2, Welder3, Welder4: Welder names and IDs in format "Name (ID)"

**CRITICAL DATA TRANSFORMATION:**
The raw data contains weld-level records. Users don't want to see individual weld rows - they want a WELDER SUMMARY.

**YOU MUST AGGREGATE THE DATA** by welder to show:
1. Extract all unique welders from Welder1, Welder2, Welder3, Welder4 fields
2. Parse welder name and ID separately (format: "Name (ID)")
3. Count total welds per welder (a welder can appear in multiple Welder1/2/3/4 positions across welds)
4. Count welds by category (Production, Repaired, CutOut) for each welder

AGGREGATED TABLE STRUCTURE:
**ALWAYS show this aggregated summary table:**

Column 1: Welder Name (extracted from "Name (ID)" format)
Column 2: Welder ID (extracted from "Name (ID)" format)
Column 3: Total Welds (count of welds this welder worked on)
Column 4: Production (count of Production welds)
Column 5: Repaired (count of Repaired welds)
Column 6: CutOut (count of CutOut welds)

Sort by: Total Welds descending (show most active welders first)

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key takeaways + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- If user says "yes", "show all", "full data", or similar → Display full aggregated table
- **Skip key takeaways** (already provided in previous message)
- Just provide one-sentence confirmation and full aggregated table

RESPONSE FORMAT:
1. **One-sentence answer** to user's specific question (no headings, no extra commentary)
   - Example: "12 welders worked on work order 100500514."
   - Example: "John Doe worked on 25 welds in work order 100500514."

2. **Table Contents** (CONDITIONAL based on context):
   - **If this is INITIAL response**: **DO NOT display any table**

   - **If this is FOLLOW-UP requesting full data**: Display full aggregated table:
     - **Default columns**: Welder Name | Welder ID(ITS ID) | Total Welds | Production | Repaired | CutOut
     - Sort by Total Welds descending
     - Use clear formatting and handle null values with "-"
     - **CRITICAL**: This is an aggregated summary, NOT individual weld rows
     - Do not consider empty welder fields as a unique welder. Ignore empty welder row when displaying the table

3. **Key Takeaways** (CONDITIONAL - only on initial response):
   - **Show key takeaways ONLY on initial response**
   - **Skip key takeaways on follow-up response**
   - Provide insights: top welder by total welds, category distribution if relevant
   - Keep factual and concise

4. **Data Request Prompt** (only on initial response):
   - Inform the user and ask if they need the full data
   - Examples: "Would you like to see the full list?", "Would you like me to display all welders?"
   - **CRITICAL**: Never use the word "dataset"
   - **DO NOT** add other questions or suggestions

CRITICAL RULES:
- **NEVER show individual weld rows** - always aggregate by welder
- Parse welder name and ID from "Name (ID)" format into separate columns
- Count welds per welder across all Welder1/2/3/4 positions
- Sort by Total Welds descending
- **On initial response: NO TABLE** - just answer + key takeaways + prompt
- **On follow-up for full data: FULL AGGREGATED TABLE** + NO key takeaways
- Answer the user's specific question directly
- **NEVER use the word "dataset"** - use "records", "data", "welds" instead
- **NEVER add unsolicited follow-up questions or suggestions**

For any counting questions, refer to the aggregated welder count, not the raw weld record count.
=== END GetWelderNameDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
"""
