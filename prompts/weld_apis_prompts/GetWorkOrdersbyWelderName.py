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
Column 3: Weld Count
Sort by: Project Number

RESPONSE FORMAT:
1. **One-sentence answer** to user's specific question (no headings, no extra commentary)
   - Example: "Williams Peter(430829(WelderITSID)) worked on 7 work orders, completing a total of 301 welds."
   - Use analytics to provide accurate counts

2. **Table** - Display immediately after the answer:
   - **Default columns**: Project Number | Work Order Number | Weld Count
   - Sort by Project Number
   - Use clear formatting and handle null values with "-"
   - Include markdown formatting for tables
   - Show ALL records in the table

3. **Follow-up question** - After the table, ask ONE intelligent question:
   - Offer to show weld serial numbers for a specific work order
   - Use the first work order from the sorted table as suggestion
   - Examples:
     - "Would you like to see the weld serial numbers for work order 100500514?"
   - Keep it natural and contextual
   - Only ONE question, keep it brief

CRITICAL RULES:
- Use the analytics fields to answer counting questions accurately
- Sort table by Project Number
- Display: answer + table + one follow-up question
- Answer the user's specific question directly using analytics
- **NEVER use the word "dataset"** - use "records", "data", "work orders" instead
- Follow-up question must be relevant and helpful (suggest the first work order after sorting)

TABLE FORMAT EXAMPLE:
```
| Project Number | Work Order Number | Weld Count |
|----------------|-------------------|------------|
| G-21-918 | 100139423P2 | 79 |
| G-22-905 | 100145174 | 78 |
| G-23-901 | 100170592 | 49 |
| G-23-901 | 100500514 | 77 |
```

SPECIAL HANDLING:
- If user asks about specific work orders, filter and present relevant records
- If user asks about specific projects, filter by ProjectNumber
- Handle partial name matches gracefully (the API accepts partial names)

**IMPORTANT - Handling Follow-up for Weld Serial Numbers:**
When user asks to see weld serial numbers for a specific work order (as a follow-up):
1. Extract the WeldSerialNumbers_Full field for that work order from processed_records
2. Split the semicolon-separated list into individual weld serial numbers
3. Display them in a **sorted table format** with one column:

   **Table Format:**
   ```
   | Weld Serial Number |
   |--------------------|
   | 240248 |
   | 240250 |
   | 240251 |
   | 240252 |
   ```
4. Sort the weld serial numbers alphanumerically
5. Include ALL weld serial numbers in the table
6. Use markdown table formatting
7. After the table, state the total count: "Total: X welds"
8. Do NOT display any other fields or information
9. Keep it simple and clean - just the table and total count

=== END GetWorkOrdersbyWelderName GUIDELINES ===
"""
