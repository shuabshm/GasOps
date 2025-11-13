def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWeldsbyTRIndicationandWorkOrderNumber API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_parameters = api_parameters if api_parameters else {}

    return f"""
=== GetWeldsbyTRIndicationandWorkOrderNumber API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns welds that have a specific TR indication type in a work order, showing how many times the indication appears on each weld.

RESPONSE STRUCTURE:
The API returns a list of welds filtered by specific indication type.

AVAILABLE FIELDS:
- WeldSerialNumber: Weld serial number identifier
- WorkOrderNumber: Work order number (required filter parameter - always same for all records)
- Indication: Type of TR indication (required filter parameter - always same for all records, e.g., Porosity, Slag Inclusions, Foreign Material, Burn Through, Undercut, Other (enter in remarks))
- IndicationCount: Number of times the indication appears on this weld

FIELD DISPLAY LOGIC:

**Core Fields (ALWAYS show):**
- WeldSerialNumber
- IndicationCount

**Smart Field Hiding (filter_parameters):**
- **WorkOrderNumber**: ALWAYS hide (required filter parameter - always same for all records)
- **Indication**: ALWAYS hide (required filter parameter - always same for all records)

**Why hide Indication?** Since TRIndication is a required input parameter, all rows will have the same indication type. The indication type is already mentioned in the one-sentence answer, so no need to repeat it in every table row.

**Result**: Display only WeldSerialNumber + IndicationCount columns

Field Display Rules:
- Use "-" for null/empty values
- Maintain column ordering: WeldSerialNumber, IndicationCount
- Use clear column headers: "Weld Serial Number", "Indication Count"

TABLE SORTING:
**CRITICAL**: ALWAYS sort by first column in descending order before displaying any table then the indication count.

TARGETED KEY INSIGHTS:
**When to show:**
- Show on initial query response (MODE 1)
- Skip on follow-up when user requests full data (MODE 2)

**Focus on indication count distribution and quality concerns:**

**Always include:**
- Total weld count with this indication
- IndicationCount distribution (highest, lowest, average if useful)
- Welds with highest counts that need priority attention
- Quality concern emphasis (if high counts indicate problems)
- If sample displayed, provide overall statistics for full dataset

**Examples:**
- "Total 12 welds affected, indication counts range from 1 to 3 occurrences per weld"
- "Weld 250244 has the highest count at 2 occurrences, requiring priority attention"
- "Most welds (8 of 12) have only 1 occurrence, indicating isolated issues"

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent. Do not include any headings, additional commentary, or explanations.

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence summary answer to the user's specific question from a business perspective.
    * Use total record count as the total count when reporting the volume
    * **Mention indication type, work order, total count, and weld with highest count**
    * Examples:
        * "3 welds have Porosity indication in work order 100500514, with weld 240916 having the highest count at 2 occurrences."
        * "5 welds show Undercut in work order 100500514, with weld 250150 having 2 occurrences."

2.  **Key Takeaways(Do not include any headings like "Key Takeaways" or similar):** Provide targeted insights as separate bullet points following the **TARGETED KEY INSIGHTS** guidelines.
    * Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
    * **Focus on indication count distribution and quality concerns.**

3.  **Data Request Prompt:** Conclude the response with a single-line prompt asking if they want the full data.
    * Examples: "Would you like to see all welds?", "Need the complete list?", "Should I display the full data?"
    * **CRITICAL**: Never use the word "dataset". **DO NOT** add any other questions or suggestions.

4.  **Table Display:** **STRICTLY DO NOT** display any table in this mode.

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table using phrases like: "show me", "display the data", "yes", "show all", "full data", "full list", or similar.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence confirmation specific to the data being displayed.
    * Example: "Here is the full list of welds with [Indication Type] TR indication, grouped by weld serial number."

2.  **Key Takeaways:** **STRICTLY DO NOT** include any key takeaways.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt or any other unsolicited questions/suggestions.

4.  **Table Display:** Display the full table with **ALL rows**.
    * **ALWAYS show:** WeldSerialNumber, IndicationCount
    * **ALWAYS hide:** WorkOrderNumber (filter_parameters), Indication (filter_parameters)
    * **ALWAYS sort by first column in descending order before displaying any table then the indication count.
    * Use clear formatting and handle null values with "-".

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "welds", "records", "data" instead
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**
- Always use absolute numbers for counts not percentages
- Core fields: ALWAYS show WeldSerialNumber, IndicationCount
- Filter fields: ALWAYS hide WorkOrderNumber and Indication (both are required filter parameters)
- Sorting: ALWAYS sort by first column in descending order before displaying any table then the indication count.
- Key insights: Focus on count distribution and priority welds
- One-sentence answer: Mention indication type, work order, total count, highest count weld

For any counting questions, the total is [X] weld records. Focus on providing targeted analysis of indication count distribution and identifying welds requiring priority attention.
=== END GetWeldsbyTRIndicationandWorkOrderNumber GUIDELINES ===
"""
