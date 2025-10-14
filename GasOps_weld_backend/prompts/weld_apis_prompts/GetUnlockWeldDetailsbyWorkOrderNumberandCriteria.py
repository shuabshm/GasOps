def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetUnlockWeldDetailsbyWorkOrderNumberandCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetUnlockWeldDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API is a workflow/task management API that tracks welds that have been unlocked for editing and their update status. Users need to identify pending work and track accountability.

AVAILABLE FIELDS:
- WorkOrderNumber: Work order identifier
- ProjectNumber: Project identifier
- WeldCategory: Category of weld (Production, Repaired, CutOut)
- WeldSerialNumber: Unique weld identifier
- ContractorName: Name of the contractor
- Welder1-4: Welder names and IDs
- ContractorCWIName: Contractor CWI name
- CWIName: CWI inspector name
- UnlockedBy: Name of user who unlocked the weld
- UnlockedDate: Date when weld was unlocked
- UpdateCompleted: Whether update is completed (Yes/No)
- UpdatedBy: Name of user who updated the weld
- UpdatedDate: Date when weld was updated

**CRITICAL CONCEPT**: Welds pending to be edited have **null or blank UpdatedDate**

CORE FIELDS (Revised for Workflow Tracking):

**Always show:**
- WeldSerialNumber (what needs updating)
- UnlockedBy (who's responsible)
- UnlockedDate (when unlocked - urgency indicator)
- UpdateCompleted (Yes/No - status at a glance)

**Smart conditional display:**
- UpdatedDate - Show/hide based on query context (see rules below)
- UpdatedBy - Only show if user asks about it

**Hide by default:**
- WorkOrderNumber (always same - already in context)
- ProjectNumber (usually same - hide unless varies)

SMART FIELD HIDING LOGIC:

**WorkOrderNumber:** Always hide (same for all records - in input parameter)

**ProjectNumber:** Hide unless values vary across records

**UpdatedDate Visibility (Smart Context-Aware Display):**

| User Query Pattern | UpdatedDate Column |
|-------------------|-------------------|
| "pending", "not updated", "needs update", "to be edited" | HIDE (all null anyway - redundant) |
| "completed", "updated welds", "all unlocked welds" | SHOW (useful to see when completed) |
| "updated by", "update timeline", "duration", "how long" | SHOW (needed for analysis) |
| General/ambiguous query | SHOW (safer to include for context) |

**Other fields:** Only show when specifically requested by user query

ACTION-ORIENTED TABLE SORTING:
**CRITICAL**: Sort to put action items requiring attention at the top!

**Primary sort:** UpdateCompleted (ascending) → "No" first (pending items on top)
**Secondary sort:** UnlockedDate (ascending) → Oldest first (most urgent pending on top)

**Result:** Pending items appear first, with most urgent (oldest unlocked) at the very top!

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key insights + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- Display full table with all rows
- **Skip key insights**

KEY INSIGHTS GUIDELINES (Workflow-Focused):
**When to show:**
- Show on initial query response
- Skip on follow-up when user requests full data

**What to include (workflow tracking focus):**

1. **Update completion status breakdown (ALWAYS include):**
   - "Update status: 60% completed (15 welds), 40% pending (10 welds)"
   - If all completed: "All unlocked welds have been updated"
   - If all pending: "All 25 unlocked welds are still pending updates"
   - **CRITICAL**: Prominently show pending count - this is what users need for action

2. **User activity distribution (if multiple users):**
   - Unlocked by distribution: "Unlocked by: Nikita (12 welds), John (8 welds), Sarah (5 welds)"
   - Updated by distribution (if UpdatedBy shown): "Updated by: John (10 welds), Sarah (5 welds)"
   - Skip if only one user

3. **Category breakdown (only if WeldCategory shown and relevant):**
   - "Pending updates by category: 60% Production (6 welds), 40% Repaired (4 welds)"

4. **Final summary (ONLY if alarming or actionable):**
   - "10 welds have been unlocked for more than 7 days but remain pending"
   - "High number of pending updates (20+) may require attention"

**Format Requirements:**
- Each insight as separate bullet point on its own line
- Never merge into paragraph
- Use percentages + absolute counts
- Factual observations only
- Focus on actionable information (pending work)
- **ONLY state factual observations**
- **DO NOT include recommendations**

RESPONSE FORMAT:
1. **One-sentence answer (Action-Oriented)**

   **If pending > 0 (action needed):**
   - "[X] welds are pending updates in work order [Y] ([Z] already completed)"
   - "[X] welds need to be updated in work order [Y]"
   - Examples:
     - "5 welds are pending updates in work order 100500514 (20 already completed)"
     - "10 welds need to be updated in work order 100500514"

   **If all completed (no action needed):**
   - "All [X] unlocked welds in work order [Y] have been updated"
   - Example: "All 25 unlocked welds in work order 100500514 have been updated"

   **Highlight what needs action first!** Use total record count for totals.

2. **Table Contents** (CONDITIONAL based on response type):
   - **Initial Response**: DO NOT display any table

   - **Follow-up Response (when user requests full data)**: Display full table with ALL rows:
     - Always show: WeldSerialNumber, UnlockedBy, UnlockedDate, UpdateCompleted
     - Smart display: UpdatedDate (based on context rules above)
     - Additional fields: Only if user query requests them
     - Sort by: UpdateCompleted (No first), then UnlockedDate (oldest first)
     - Show ALL rows - no limits
     - Use clear formatting and handle null values with "-"

3. **Key Insights** (CONDITIONAL - skip on follow-up):
   - **Show key insights** if this is initial response
   - **Skip key insights** if this is follow-up response to show full data
   - Follow Workflow-Focused Guidelines above
   - Each bullet on its own line
   - Focus on update completion status, user activity, and actionable information

4. **Data Request Prompt** (only on initial response):
   - Inform the user that they can request the full data
   - Keep it natural and conversational
   - Examples: "Would you like to see the detailed breakdown?", "Need the complete list?", "Should I display the full data?"
   - **CRITICAL**: Never use the word "dataset" - use "welds", "list", "data", "records" instead
   - **DO NOT** add any other questions, suggestions, or offers for additional analysis

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "welds", "unlocked welds", "records" instead
- Always show core fields: WeldSerialNumber, UnlockedBy, UnlockedDate, UpdateCompleted
- Smart display UpdatedDate based on query context (hide for "pending" queries, show for others)
- Hide WorkOrderNumber (always same)
- Hide ProjectNumber unless varies
- Sort with pending items first (UpdateCompleted="No"), oldest first (UnlockedDate ascending)
- **Initial Response: NO TABLE** - just answer + key insights + data request prompt
- **Follow-up Response: FULL TABLE with ALL rows** - no key insights
- Key insights: workflow-focused, highlight pending work prominently
- One-sentence answer: action-oriented, pending count first if applicable
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**

For any counting questions, the total is [X] unlock records. This is a workflow/task management API - focus on actionable information and pending work identification.
=== END GetUnlockWeldDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
"""
