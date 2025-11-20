def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for Weld Map Status queries
    
    Args:
        api_parameters (dict): Optional dictionary of API filter parameters
        
    Returns:
        str: The formatted API-specific prompt
    """
    return f"""
=== Weld Map Status Query - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines for weld map queries.**

This query provides weld map status information with inspection details.

AVAILABLE FIELDS (Display these columns only):
- ProjectNumber (as "Project Number")
- WeldCategory (as "Weld Category")
- WeldSerialNumber (as "Weld Serial#")
- AddedtoWeldMap (as "Added to Weld Map")
- Welders (consolidated from Welder1-4)
- CWIName, CWIResult, CWICompletionDate
- NDEName, NDEResult, NDECompletionDate
- CRIName, CRIResult, CRICompletionDate
- TRName, TRResult, TRCompletionDate

STATISTICS AVAILABLE:
- total_unique_welds: Count of unique weld serial numbers
- added_to_map_yes: Count of welds with AddedtoWeldMap = "Yes"
- added_to_map_no: Count of welds with AddedtoWeldMap = "No"

RESPONSE FORMAT:

**For status queries** (e.g., "show me the status of weld map for work order 123"):
1. Start with a clear summary sentence:
   "Work order **123** has **X unique welds**, with **Y added to the weld map** and **Z not yet added**."

2. Add section header: "Here's the details:"

3. If there are welds NOT added to the map (AddedtoWeldMap = "No"), ALWAYS show them using TWO bullet points per weld:
   - First bullet: "- Weld **[Serial#]** ([Category] category) was welded by [Welder names]."
   - Second bullet: "- The CWI inspection was [result] on [date], however the NDE inspection was [result] on [date], and the CRI was also [result] on [date]."
   - Example format:
     "- Weld **251528** (CutOut category) was welded by Post Aaron."
     "- The CWI inspection was accepted on 07/08/2025, however the NDE inspection was rejected on 07/20/2025, and the CRI was also rejected on 07/16/2025."
   - If inspection is pending, say "The CWI inspection was accepted on [date], however the NDE inspection is pending, and the CRI is not yet completed."
   - Use "however" to connect contrasting results
   - Use "and" to add additional inspection results
   - Add a blank line between different welds for readability

4. After showing all welds not added to map, add context:
   "This means almost all welds for this work order are already included in the weld map, with just Z outstanding."
   (If Z = 0, say "All welds for this work order are included in the weld map.")

5. End with: "Would you like me to show you the **detailed list with inspection results** for all welds in this work order? That way you can see the CWI, NDE, and CRI outcomes for each."

**For specific filter queries** (e.g., "Are there any weld maps with no in work order 123"):
1. Answer directly:
   "Yes, there are **X welds** not yet added to the weld map in work order **123**."
   OR
   "No, all welds in work order **123** have been added to the weld map."

2. Add section header: "Here's the details:"

3. Show weld details using TWO bullet points per weld (same format as status queries):
   - First bullet: "- Weld **[Serial#]** ([Category] category) was welded by [Welder names]."
   - Second bullet: "- The CWI inspection was [result] on [date], however the NDE inspection was [result] on [date], and the CRI was also [result] on [date]."
   - Example:
     "- Weld **251528** (CutOut category) was welded by Post Aaron."
     "- The CWI inspection was accepted on 07/08/2025, however the NDE inspection was rejected on 07/20/2025, and the CRI was also rejected on 07/16/2025."
   - Add blank line between different welds

4. Ask if user wants more details:
   "Would you like to see the complete table with all inspection details for these welds?"

**When user requests table/details**:
Display full table with ALL columns listed above, showing all matching records.

TABLE FORMAT:
| Project Number | Weld Category | Weld Serial# | Added to Weld Map | Welders | CWI Name | CWI Result | CWI Date | NDE Name | NDE Result | NDE Date | CRI Name | CRI Result | CRI Date | TR Name | TR Result | TR Date |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

CRITICAL RULES:
- Always use statistics from the transformed data (total_unique_welds, added_to_map_yes, added_to_map_no)
- ALWAYS show weld details for welds with AddedtoWeldMap = "No" in the initial response
- Use TWO bullet points per weld for easy readability
- First bullet: Weld identification and welders
- Second bullet: All inspection results with dates
- Use dash (-) for bullet points, not dot (•)
- Use conversational, flowing language within each sentence
- Use bold text (**) for emphasis on numbers, weld serial numbers, and work order numbers
- Never show full table in initial response unless explicitly requested
- Focus on answering the specific question asked
- Provide context about weld map status
- Say "pending" or "is not yet completed" for empty inspection fields
- Use "however" to contrast different inspection results
- Use "and the [inspection] was also [result]" for additional inspections
- Add blank line between different welds for visual separation
- Access weld details from the "weld_map_records" array in the data

DATA ACCESS:
- Use data_representation["weld_map_records"] to find welds where AddedtoWeldMap = "No"
- Each record in weld_map_records has these fields:
  * WeldSerialNumber
  * WeldCategory  
  * AddedtoWeldMap
  * Welders (already consolidated)
  * CWIResult, CWICompletionDate
  * NDEResult, NDECompletionDate
  * CRIResult, CRICompletionDate
  * TRResult, TRCompletionDate

=== END Weld Map Status Guidelines ===
"""