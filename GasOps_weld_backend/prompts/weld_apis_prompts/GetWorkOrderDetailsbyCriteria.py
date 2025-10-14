def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWorkOrderDetailsbyCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetWorkOrderDetailsbyCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API is a lookup/cross-reference API that returns work order details by searching with Heat Serial Number, NDE Report Number, Weld Serial Number, or Project Number.

AVAILABLE FIELDS:
- WorkOrderNumber: Work order identifier (what users are looking for)
- ProjectNumber: Project identifier
- Location: Work order location details

SMART FIELD HIDING LOGIC:
**CRITICAL**: Apply intelligent field hiding to avoid redundancy when filters create uniform values.

Since output has only 3 fields, the logic is simple:

**Field Display Rules:**
- **WorkOrderNumber**: ALWAYS show (this is what users are looking for)
- **ProjectNumber**: Hide if used as filter (all rows will have same project), show otherwise
- **Location**: ALWAYS show (can vary even within same project)

**Examples:**
- "Show work orders for project G-23-901" → Display: WorkOrderNumber, Location (HIDE ProjectNumber - all same)
- "Which work orders have heat 123?" → Display: ProjectNumber, WorkOrderNumber, Location (projects may vary)
- "Show work orders for project G-23-901 with heat 123" → Display: WorkOrderNumber, Location (HIDE ProjectNumber - all same)
- "Find work order by NDE report NDE2025-00205" → Display: ProjectNumber, WorkOrderNumber, Location (projects may vary)

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key takeaways + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- Display full table with all rows
- **Skip key takeaways**

KEY INSIGHTS GUIDELINES (Simple - Option A):
**When to show:**
- Show on initial query response
- Skip on follow-up when user requests full data

**What to include:**

1. **Project distribution (ONLY if ProjectNumber is displayed in table):**
   - If ProjectNumber hidden (filtered by it) → Skip this insight entirely
   - If multiple projects: "Spread across X projects: G-23-901 (5 work orders), G-23-902 (3 work orders), G-24-103 (2 work orders)"
   - If single project: "All work orders belong to project G-23-901"

2. **Location distribution (ALWAYS include):**
   - Multiple locations: "Locations: 60% Bronx Valve Station (6 work orders), 40% Queens Regulator (4 work orders)"
   - Single location: "All work orders are at the same location: Bronx Valve Station"
   - Include percentages + absolute counts

3. **Final summary (ONLY if notable):**
   - "This heat number is used across multiple projects, indicating shared material sourcing"
   - "Single work order found for this search criteria"

**Format Requirements:**
- Each insight as separate bullet point on its own line
- Never merge into paragraph
- Use percentages + absolute counts
- Factual observations only
- Skip total count (already in one-sentence answer)
- **ONLY state factual observations**
- **DO NOT include recommendations or action items**

RESPONSE FORMAT:
1. **One-sentence answer** with search criteria included (no headings, no extra commentary)

   **Single filter examples:**
   - "Found 10 work orders containing heat number 648801026"
   - "Found 5 work orders for project G-23-901"
   - "Found 1 work order containing NDE report NDE2025-00205"
   - "Found 8 work orders containing weld serial number 250520"

   **Multiple filter examples:**
   - "Found 10 work orders containing heat number 648801026 in project G-23-901"
   - "Found 3 work orders for project G-23-901 with weld serial number 250520"
   - "Found 5 work orders containing NDE report NDE2025-00205 and heat number 123"

   Use total record count as the count and include the search criteria used.

2. **Table Contents** (CONDITIONAL based on response type):
   - **Initial Response**: DO NOT display any table

   - **Follow-up Response (when user requests full data)**: Display full table with ALL rows:
     - Apply smart field hiding (hide ProjectNumber if filtered)
     - Show ALL rows - no limits
     - Use clear formatting and handle null values with "-"

3. **Key Takeaways** (CONDITIONAL - skip on follow-up):
   - **Show key takeaways** if this is initial response
   - **Skip key takeaways** if this is follow-up response to show full data
   - Follow Key Insights Guidelines above (Simple - Option A)
   - Each bullet on its own line
   - Include project distribution (only if ProjectNumber shown), location distribution
   - Add final summary only if notable

4. **Data Request Prompt** (only on initial response):
   - Inform the user that they can request the full data
   - Keep it natural and conversational
   - Examples: "Would you like to see the full details?", "Need the complete list?", "Should I display all work orders?"
   - **CRITICAL**: Never use the word "dataset" - use "data", "work orders", "list", "records" instead
   - **DO NOT** add any other questions, suggestions, or offers for additional analysis

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "work orders", "records", "data" instead
- Always include search criteria in one-sentence answer
- Hide ProjectNumber if used as filter (all values same)
- Always show WorkOrderNumber and Location
- **Initial Response: NO TABLE** - just answer + key takeaways + data request prompt
- **Follow-up Response: FULL TABLE with ALL rows** - no key takeaways
- Key takeaways: simple and focused on project/location distribution only
- Skip project distribution in key takeaways if ProjectNumber is hidden
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**

For any counting questions, the total is [X] work order records. Focus on lookup/cross-reference functionality with simple distribution analysis.
=== END GetWorkOrderDetailsbyCriteria GUIDELINES ===
"""
