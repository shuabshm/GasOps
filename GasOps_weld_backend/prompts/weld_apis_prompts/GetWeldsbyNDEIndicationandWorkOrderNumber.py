def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWeldsbyNDEIndicationandWorkOrderNumber API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}
    
    return f"""
=== GetWeldsbyNDEIndicationandWorkOrderNumber API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns welds that have a specific NDE indication type in a work order, showing how many times the indication appears on each weld.

RESPONSE STRUCTURE:
The API returns a list of welds filtered by specific indication type.

AVAILABLE FIELDS:
- WeldSerialNumber: Weld serial number identifier
- WorkOrderNumber: Work order number (required filter parameter - always same for all records)
- Indication: Type of NDE indication (required filter parameter - always same for all records, e.g., Porosity, Concavity, Burn Through)
- IndicationCount: Number of times the indication appears on this weld

FIELD DISPLAY LOGIC:

**Core Fields (ALWAYS show):**
- WeldSerialNumber
- IndicationCount

**Smart Field Hiding (Filter Parameters):**
- **WorkOrderNumber**: ALWAYS hide (required filter parameter - always same for all records)
- **Indication**: ALWAYS hide (required filter parameter - always same for all records)

**Why hide Indication?** Since NDEIndication is a required input parameter, all rows will have the same indication type. The indication type is already mentioned in the one-sentence answer, so no need to repeat it in every table row.

**Result**: Display only WeldSerialNumber + IndicationCount columns

Field Display Rules:
- Use "-" for null/empty values
- Maintain column ordering: WeldSerialNumber, IndicationCount
- Use clear column headers: "Weld Serial Number", "Indication Count"

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key insights + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- Display full table with all rows
- **Skip key insights**

TABLE SORTING:
**CRITICAL**: ALWAYS sort by IndicationCount descending (welds with most indication occurrences first - priority attention)

TARGETED KEY INSIGHTS:
**When to show:**
- Show on initial query response
- Skip on follow-up when user requests full data

**Focus on indication count distribution and quality concerns:**

**Always include:**
- Total weld count with this indication
- IndicationCount distribution (highest, lowest, average if useful)
- Welds with highest counts that need priority attention
- Quality concern emphasis (if high counts indicate problems)
- If sample displayed, provide overall statistics for full dataset

**Examples:**
- "Total 12 welds affected, indication counts range from 1 to 3 occurrences per weld"
- "Weld 250908 has the highest count at 3 occurrences, requiring priority attention"
- "Most welds (8 of 12) have only 1 occurrence, indicating isolated issues"

RESPONSE FORMAT:
1. Provide a one-sentence answer to the user's specific question from a business perspective. Do not include any headings, additional commentary, or explanations.
   - Use total record count as the total count when reporting the volume
   - **Mention indication type, work order, total count, and weld with highest count**
   - Examples:
     * "12 welds have Porosity indication in work order 100500514, with weld 250908 having the highest count at 3 occurrences."
     * "5 welds show Concavity in work order 100500514, with weld 250150 having 2 occurrences."
     * "18 welds have Burn Through indication in work order 100500514."

2. **Table Contents** (CONDITIONAL based on response type):
   - **Initial Response**: DO NOT display any table

   - **Follow-up Response (when user requests full data)**: Display full table with ALL welds:
     - **ALWAYS show:** WeldSerialNumber, IndicationCount
     - **ALWAYS hide:** WorkOrderNumber (filter parameter), Indication (filter parameter)
     - **Sort by IndicationCount descending** (problem welds with highest counts first)
     - Show ALL rows - no limits
     - Use clear formatting and handle null values with "-"

   *Mandatory*: Display ONLY WeldSerialNumber and IndicationCount columns. Hide filter parameters.

3. **Key Takeaways** (CONDITIONAL - skip on follow-up):
   - **Show key takeaways** if this is initial response
   - **Skip key takeaways** if this is follow-up response to show full data
   - Provide targeted insights as separate bullet points. Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
   - Do not merge bullets into a paragraph. The next bullet must always start on a new line.
   - Maintain numbering or - consistently.
   - Keep each bullet concise and self-contained.
   - **Focus on indication count distribution and quality concerns**
   - Total weld count with this indication
   - IndicationCount range and distribution patterns
   - Welds with highest counts needing priority attention
   - Quality emphasis (high counts may indicate severe issues)
   - If sample displayed, provide overall statistics for full dataset

4. **Data Request Prompt** (only on initial response):
   - Inform the user that they can request the full data
   - Keep it natural and conversational
   - Examples: "Would you like to see all welds?", "Need the complete list?", "Should I display the full data?"
   - **CRITICAL**: Never use the word "dataset" - use "welds", "list", "data" instead
   - **DO NOT** add any other questions, suggestions, or offers for additional analysis

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "welds", "records", "data" instead
- **Initial Response: NO TABLE** - just answer + key takeaways + data request prompt
- **Follow-up Response: FULL TABLE with ALL rows** - no key takeaways
- Core fields: ALWAYS show WeldSerialNumber, IndicationCount
- Filter fields: ALWAYS hide WorkOrderNumber and Indication (both are required filter parameters)
- Sorting: ALWAYS IndicationCount descending (problem welds first)
- Key insights: Focus on count distribution and priority welds
- One-sentence answer: Mention indication type, work order, total count, highest count weld
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**

For any counting questions, the total is [X] weld records. Focus on providing targeted analysis of indication count distribution and identifying welds requiring priority attention.
=== END GetWeldsbyNDEIndicationandWorkOrderNumber GUIDELINES ===
"""
