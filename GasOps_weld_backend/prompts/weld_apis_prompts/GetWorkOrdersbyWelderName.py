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
- total_records: Total number of work orders the welder worked on
- total_welds: Total number of welds made by the welder across all work orders
- work_order_with_most_welds: Work order number where the welder made the most welds
- max_welds_count: Number of welds in the work order with most welds
- welder_full_name: Full name of the welder from the data
- welder_name_queried: Original welder name from the query

**CRITICAL DATA STRUCTURE:**
The data is already aggregated at the work order level. Each record represents one work order where the welder worked.

TABLE STRUCTURE:
**Default columns for the table:**

Column 1: Project Number
Column 2: Work Order Number
Sort by: Project Number

RESPONSE FORMAT:
1. **One-sentence answer** to user's specific question (no headings, no extra commentary)
   - Example: "Williams Peter worked on 7 work orders, completing a total of 301 welds."
   - Use analytics to provide accurate counts

2. **Table** - Display immediately after the answer:
   - **Default columns**: Project Number | Work Order Number
   - Sort by Project Number
   - Use clear formatting and handle null values with "-"
   - Include markdown formatting for tables
   - Show ALL records in the table

CRITICAL RULES:
- Use the analytics fields to answer counting questions accurately
- Sort table by Project Number
- Display one-sentence answer followed immediately by the full table
- No key takeaways, no insights, no follow-up questions
- Answer the user's specific question directly using analytics
- **NEVER use the word "dataset"** - use "records", "data", "work orders" instead
- **NEVER add unsolicited follow-up questions or suggestions**

TABLE FORMAT EXAMPLE:
```
| Project Number | Work Order Number |
|----------------|-------------------|
| G-21-918 | 100139423P2 |
| G-22-905 | 100145174 |
| G-23-901 | 100170592 |
| G-23-901 | 100500514 |
```

SPECIAL HANDLING:
- If user asks about specific work orders, filter and present relevant records
- If user asks about specific projects, filter by ProjectNumber
- Handle partial name matches gracefully (the API accepts partial names)

=== END GetWorkOrdersbyWelderName GUIDELINES ===
"""
