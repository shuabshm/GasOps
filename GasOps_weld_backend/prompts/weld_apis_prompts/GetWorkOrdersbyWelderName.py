def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWorkOrdersbyWelderName API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    return f"""
=== GetWorkOrdersbyWelderName API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API provides a list of work orders where there are welds made by a specific welder, along with weld counts and serial numbers.

AVAILABLE FIELDS (Processed Data):
From processed_records:
- WorkOrderNumber: Work order identifier
- ProjectNumber: Project identifier
- WelderName: Full welder name (e.g., "Vandaly Brian")
- WelderITSID: Welder ITS ID
- WeldCount: Number of welds made by this welder in this work order
- WeldSerialNumbers_Truncated: Truncated weld serial numbers (e.g., "240248; 240250; 240251... (150 total)")
- WeldSerialNumbers_Full: Complete semicolon-separated list of all weld serial numbers

From analytics:
- total_work_orders: Total number of work orders the welder worked on
- total_welds: Total number of welds made by the welder across all work orders
- work_order_with_most_welds: Work order number where the welder made the most welds
- max_welds_count: Number of welds in the work order with most welds
- welder_full_name: Full name of the welder from the data
- welder_name_queried: Original welder name from the query

**CRITICAL DATA STRUCTURE:**
The data is already aggregated at the work order level. Each record represents one work order where the welder worked.

TABLE STRUCTURE:
**Default columns for the table:**

Column 1: Work Order Number
Column 2: Project Number
Column 3: Weld Count
Column 4: Weld Serial Numbers (use WeldSerialNumbers_Truncated)

Sort by: Weld Count descending (show work orders with most welds first)

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key takeaways + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- If user says "yes", "show all", "full data", or similar → Display full table
- **Skip key takeaways** (already provided in previous message)
- Just provide one-sentence confirmation and full table

RESPONSE FORMAT:
1. **One-sentence answer** to user's specific question (no headings, no extra commentary)
   - Example: "Vandaly Brian worked on 4 work orders, completing a total of 217 welds."
   - Example: "The welder has worked on 15 different work orders across 5 projects."
   - Use analytics to provide accurate counts

2. **Table Contents** (CONDITIONAL based on context):
   - **If this is INITIAL response**: **DO NOT display any table**

   - **If this is FOLLOW-UP requesting full data**: Display full table:
     - **Default columns**: Work Order Number | Project Number | Weld Count | Weld Serial Numbers
     - Sort by Weld Count descending (most active work orders first)
     - Use WeldSerialNumbers_Truncated field (shows first 3 + count)
     - Use clear formatting and handle null values with "-"
     - Include markdown formatting for tables

3. **Key Takeaways** (CONDITIONAL - only on initial response):
   - **Show key takeaways ONLY on initial response**
   - **Skip key takeaways on follow-up response**
   - Provide insights using analytics:
     - Total work orders and total welds
     - Work order with most welds and its count
     - Any notable patterns (e.g., concentration in specific projects)
   - Keep factual and concise

4. **Data Request Prompt** (only on initial response):
   - Inform the user and ask if they need the full data
   - Examples: "Would you like to see the full list of work orders?", "Would you like me to display all work orders?"
   - **CRITICAL**: Never use the word "dataset"
   - **DO NOT** add other questions or suggestions

CRITICAL RULES:
- Use the analytics fields to answer counting questions accurately
- Sort table by Weld Count descending
- Use WeldSerialNumbers_Truncated for display (not the full list)
- **On initial response: NO TABLE** - just answer + key takeaways + prompt
- **On follow-up for full data: FULL TABLE** + NO key takeaways
- Answer the user's specific question directly using analytics
- **NEVER use the word "dataset"** - use "records", "data", "work orders" instead
- **NEVER add unsolicited follow-up questions or suggestions**

TABLE FORMAT EXAMPLE:
```
| Work Order Number | Project Number | Weld Count | Weld Serial Numbers |
|-------------------|----------------|------------|---------------------|
| 100500514 | G-23-901 | 150 | 240248; 240250; 240251... (150 total) |
| 100145174 | G-22-905 | 52 | 240984-R; 241152-R; 241158... (52 total) |
| 100139423P2 | G-21-918 | 12 | 251921; 251924; 251926... (12 total) |
| 100170592 | G-23-901 | 3 | 240348; 240352; 250819 |
```

SPECIAL HANDLING:
- If user asks for weld serial numbers in full, use WeldSerialNumbers_Full field
- If user asks about specific work orders, filter and present relevant records
- If user asks about specific projects, group or filter by ProjectNumber
- Handle partial name matches gracefully (the API accepts partial names)

=== END GetWorkOrdersbyWelderName GUIDELINES ===
"""
