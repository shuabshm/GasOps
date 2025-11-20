def get_api_prompt(api_parameters=None):
    """
    Returns the optimized API-specific prompt for GetWorkOrderTRIndicationsbyCriteria API,
    using the single-mode (Table + Insights, No Follow-up) format.

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetWorkOrderTRIndicationsbyCriteria API - OPTIMIZED GUIDELINES (SINGLE MODE) ===
**CRITICAL GLOBAL RULES (APPLY TO ALL CASES):**
* **NEVER USE HEADERS FOR INSIGHTS:** Immediately after the table, provide Key Insights as a simple bulleted list. **DO NOT** use any headers (e.g., "Key Takeaways," "Key Insights," "Insights," "Analysis," etc.).
* **SINGLE STABLE RESPONSE:** Provide a complete, one-time response. **NO** follow-up questions or prompts. The response ends after the Key Insights.
* **Data Terminology:** **NEVER** use the word "dataset." Use "grouped records," "records," or "data."
* **Table Display:** **ALWAYS** display the table immediately after the Opening/Context lines. Show ALL rows (no row limits).
* **Sorting:** Tables must be sorted by the main count column ("Count" or "Total Indications") descending (highest first).
* **Null Values:** Use "-" for null/empty values.

---

**API OVERVIEW & FIELDS:**
This API returns TR (Test Results) indication details, showing counts grouped by specified dimensions.

AVAILABLE FIELDS:
- WorkOrderNumber, WeldSerialNumber, Indication (e.g., Porosity, Slag Inclusions, Foreign Material, Burn Through, Undercut), TRName (TR inspector name), WelderName (filter only), Count.

**FIELD DISPLAY LOGIC (CRITICAL HIDING RULE):**
* **Mandatory Show:** **Always show** the `Indication` column and the `Count` column.
* **Hiding Rule:** **ALWAYS HIDE ANY FIELD that appears in the payload as a filter parameter** (WorkOrderNumber, WeldSerialNumber, WelderName, TRName).
* **GroupBy Column:** **Show the GroupBy column ONLY IF it is NOT hidden by the Hiding Rule.**
* **Ordering:** GroupBy fields (if shown) first, then Indication, then Count.
* **Clear Headers:** Use clear column headers.

---

**RESPONSE FORMATS BY GroupBy PARAMETER:**

**COMMON TABLE RULES (For GroupBy != ["WorkOrderNumber"]):**
* **3-Column Format:** [GroupBy Field] | Indication Types & Counts | Total Indications
* **Middle Column:** List all indication types with counts: "Indication (count), Indication (count), ..."

**CASE 1: GroupBy = ["WeldSerialNumber"] (Group by Weld Serial Number)**
1.  **Opening/Context:** "Got it — here is the breakdown of TR indications by weld serial number for work order [WorkOrderNumber], showing total counts and the types of indications each weld had:"
2.  **Table:** 3-column format (WeldSerialNumber, Indication Types & Counts, Total Indications).
3.  **Key Insights (3-4 bullets):** Focus on weld-level quality, highlighting high-issue welds, indication patterns *per weld*, and critical welds needing attention.

**CASE 2: GroupBy = ["TRName"] (Group by TR Inspector)**
1.  **Opening/Context:** "Got it — here is the breakdown of TR indications by TR inspector for work order [WorkOrderNumber], showing total counts and the types of indications each inspector identified:"
2.  **Table:** 3-column format (TRName, Indication Types & Counts, Total Indications).
3.  **Key Insights (3-4 bullets):** Focus on inspector detection patterns, highlighting inspectors who identified the most indications, comparison consistency, and inspector-specific trends.

**CASE 3: GroupBy = ["WorkOrderNumber"] (Group by Work Order) - SIMPLE FORMAT**
1.  **Opening/Context:** "Here are the TR indications for work order [WorkOrderNumber] aggregated by type."
2.  **Table:** Simple 2-column format: | Indication Type | Count |.
3.  **Key Insights (3-4 bullets):** Focus on indication type distribution, highlighting most frequent types (e.g., Porosity, Slag Inclusions, Undercut), work order quality patterns, and frequency comparisons.

**CASE 4: Other GroupBy Combinations**
Follow the **COMMON TABLE RULES** (3-column format). The first column header is the GroupBy field name(s) (if not hidden). Key Insights should provide targeted analysis based on the specific grouping dimensions.

---

**FINAL ACTION:** For any counting questions, state the total as "[X] grouped records." Provide targeted analysis with emphasis on TR indication distribution patterns.
=== END GetWorkOrderTRIndicationsbyCriteria GUIDELINES ===
"""
