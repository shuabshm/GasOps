# def get_api_prompt():
#     """
#     Returns the API-specific prompt for GetHeatNumberDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     return f"""
# === GetHeatNumberDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API returns heat number details for requested work order number with material traceability information.

# RESPONSE STRUCTURE:
# The API returns a flat array of heat number objects with material specifications.

# AVAILABLE FIELDS:
# - HeatNumber: Heat number identifier
# - WorkOrderNumber: Work order number (input parameter - always same for all records)
# - Asset: Asset type (e.g., Pipe, Elbows, Weldolet, Welded Tapping Fitting)
# - AssetSubcategory: Asset subcategory (e.g., Seamless Line Pipe, Welded 22.5, Spherical Tee, Weldolet)
# - Material: Material type (e.g., Steel - GRADE X42, Steel - GRADE X52, Steel)
# - Size: Size specification (e.g., 12 NPS 0.375 SCH40, 4 NPS 0.237 SCH40, 36 NPS x 4 NPS)
# - Manufacturer: Manufacturer name (e.g., Tenaris Dalmine, TD Williamson, Tectubi)

# TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY):
# **Show ONLY what the user asks for** - Display core fields + explicitly requested fields only.

# CORE FIELDS (ALWAYS show):
# - HeatNumber
# - Asset
# - AssetSubcategory

# ADDITIONAL FIELDS (ONLY show when user explicitly mentions):

# | User Query Pattern | Additional Columns to Display |
# |-------------------|------------------------------|
# | "heat numbers" / "show heat numbers" (general) | NONE - just core fields |
# | "material" / "grade" / "steel" / "X42" / "X52" | + Material |
# | "size" / "dimension" / "diameter" / "NPS" / "SCH" | + Size |
# | "manufacturer" / "supplier" / "vendor" | + Manufacturer |
# | "material and size" (multiple keywords) | + Material, Size |
# | "material and manufacturer" | + Material, Manufacturer |

# SMART FIELD HIDING LOGIC:

# **WorkOrderNumber:** ALWAYS hide (same for all records - in input parameter)

# **Asset:** Hide if used as filter parameter (all rows same), show otherwise

# **AssetSubcategory:** Hide if used as filter parameter (all rows same), show otherwise

# **Material:** Hide if used as filter parameter (all rows same), show otherwise

# **Size:** Hide if used as filter parameter (all rows same), show otherwise

# **Manufacturer:** Hide if used as filter parameter (all rows same), show otherwise

# **HeatNumber:** ALWAYS show (core identifier)

# **One-sentence answer:** If filters applied, mention them in the answer (e.g., "Work order 100500514 has 12 Pipe heat numbers with X42 material")

# Field Display Rules:
# - Use "-" for null/empty values (especially Manufacturer which is often empty)
# - Maintain consistent column ordering: HeatNumber, Asset, AssetSubcategory, Material, Size, Manufacturer
# - Use clear column headers

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key insights + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - Display full table with all rows
# - **Skip key insights**

# TABLE SORTING:
# **Default:** HeatNumber (ascending)
# **Alternative:** Group by Asset type if it provides better organization

# TARGETED KEY INSIGHTS:
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **Match insights focus to user's question:**

# | User Query Focus | Key Insights To Provide |
# |-----------------|------------------------|
# | General "heat numbers" | Asset type distribution, total count, subcategory breakdown |
# | "material" / "grade" queries | Material grade distribution, material diversity |
# | "size" queries | Size variety, common sizes, size patterns |
# | "manufacturer" queries | Manufacturer distribution, diversity, most common suppliers |
# | "asset" / "pipe" / "elbows" queries | Asset type breakdown, subcategory details |
# | Multiple aspects | Combine relevant insights, prioritize what user asked about |

# **Always include:**
# - Total heat number count
# - If sample displayed, provide overall statistics for full dataset

# RESPONSE FORMAT:
# 1. Provide a one-sentence answer to the user's specific question from a business perspective. Do not include any headings, additional commentary, or explanations.
#    - Use total record count as the total count when reporting the volume
#    - If filters applied, mention them in the answer
#    - Examples:
#      * "Work order 100500514 has 25 heat numbers across 4 asset types."
#      * "Work order 100500514 has 12 Pipe heat numbers with X42 material."
#      * "Work order 100500514 uses 3 different manufacturers for heat numbers."

# 2. **Table Contents** (CONDITIONAL based on response type):
#    - **Initial Response**: DO NOT display any table

#    - **Follow-up Response (when user requests full data)**: Display full table with ALL heat numbers:
#      - **ALWAYS show core fields:** HeatNumber, Asset, AssetSubcategory
#      - **Add fields based on query keywords** (material, size, manufacturer)
#      - **Hide filter parameter fields** that create uniform values
#      - Show ALL rows - no limits
#      - Use clear formatting and handle null values with "-"

#    *Mandatory*: Never include unnecessary columns. Always apply targeted field display and smart hiding rules.

# 3. **Key Takeaways** (CONDITIONAL - skip on follow-up)(Do not mention "key takeaways" or "insights summary" in the response):
#    - **Show key takeaways** if this is initial response
#    - **Skip key takeaways** if this is follow-up response to show full data
#    - Provide targeted insights as separate bullet points. Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
#    - Do not merge bullets into a paragraph. The next bullet must always start on a new line.
#    - Maintain numbering or - consistently.
#    - Keep each bullet concise and self-contained.
#    - **Focus insights on what user asked about** (material → material insights, size → size insights, etc.)
#    - For general queries: asset distribution, subcategory breakdown, total count
#    - For material queries: material grade distribution, diversity
#    - For manufacturer queries: supplier distribution, diversity
#    - For size queries: size patterns, common dimensions
#    - If sample displayed, provide overall statistics for full dataset

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user that they can request the full data
#    - Keep it natural and conversational
#    - Examples: "Would you like to see all heat numbers?", "Need the complete list?", "Should I display the full data?"
#    - **CRITICAL**: Never use the word "dataset" - use "heat numbers", "list", "data" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "heat numbers", "records", "data" instead
# - **Initial Response: NO TABLE** - just answer + key insights + data request prompt
# - **Follow-up Response: FULL TABLE with ALL rows** - no key insights
# - Core fields: ALWAYS show HeatNumber, Asset, AssetSubcategory (unless hidden by smart hiding)
# - Additional fields: ONLY show when user explicitly mentions them in query
# - Filter fields: HIDE if used as filter parameter (creates uniform values)
# - WorkOrderNumber: ALWAYS hide (always same - input parameter)
# - Key insights: TARGET to match user's query focus
# - One-sentence answer: Mention applied filters for context
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, the total is [X] heat number records. Focus on providing targeted analysis based on what the user asks about, with emphasis on material traceability when relevant.
# === END GetHeatNumberDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """


def get_api_prompt():
    """
    Returns the API-specific prompt for GetHeatNumberDetailsbyWorkOrderNumberandCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    return f"""
=== GetHeatNumberDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns heat number details for requested work order number with material traceability information.

RESPONSE STRUCTURE:
The API returns a flat array of heat number objects with material specifications.

AVAILABLE FIELDS:
- HeatNumber: Heat number identifier
- WorkOrderNumber: Work order number (input parameter - always same for all records)
- Asset: Asset type (e.g., Pipe, Elbows, Weldolet, Welded Tapping Fitting)
- AssetSubcategory: Asset subcategory (e.g., Seamless Line Pipe, Welded 22.5, Spherical Tee, Weldolet)
- Material: Material type (e.g., Steel - GRADE X42, Steel - GRADE X52, Steel)
- Size: Size specification (e.g., 12 NPS 0.375 SCH40, 4 NPS 0.237 SCH40, 36 NPS x 4 NPS)
- Manufacturer: Manufacturer name (e.g., Tenaris Dalmine, TD Williamson, Tectubi)

TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY):
**Show ONLY what the user asks for** - Display core fields + explicitly requested fields only.

CORE FIELDS (ALWAYS show):
- HeatNumber
- Asset
- AssetSubcategory

ADDITIONAL FIELDS (ONLY show when user explicitly mentions):

| User Query Pattern | Additional Columns to Display |
|-------------------|------------------------------|
| "heat numbers" / "show heat numbers" (general) | NONE - just core fields |
| "material" / "grade" / "steel" / "X42" / "X52" | + Material |
| "size" / "dimension" / "diameter" / "NPS" / "SCH" | + Size |
| "manufacturer" / "supplier" / "vendor" | + Manufacturer |
| "material and size" (multiple keywords) | + Material, Size |
| "material and manufacturer" | + Material, Manufacturer |

SMART FIELD HIDING LOGIC:

**WorkOrderNumber:** ALWAYS hide (same for all records - in input parameter)

**Asset:** Hide if used as filter parameter (all rows same), show otherwise

**AssetSubcategory:** Hide if used as filter parameter (all rows same), show otherwise

**Material:** Hide if used as filter parameter (all rows same), show otherwise

**Size:** Hide if used as filter parameter (all rows same), show otherwise otherwise

**Manufacturer:** Hide if used as filter parameter (all rows same), show otherwise

**HeatNumber:** ALWAYS show (core identifier)

**One-sentence answer:** If filters applied, mention them in the answer (e.g., "Work order 100500514 has 12 Pipe heat numbers with X42 material")

Field Display Rules:
- Use "-" for null/empty values (especially Manufacturer which is often empty)
- Maintain consistent column ordering: HeatNumber, Asset, AssetSubcategory, Material, Size, Manufacturer
- Use clear column headers

TARGETED KEY INSIGHTS:
**When to show:**
- Show on initial query response (MODE 1)
- Skip on follow-up when user requests full data (MODE 2)

**Match insights focus to user's question:**

| User Query Focus | Key Insights To Provide |
|-----------------|------------------------|
| General "heat numbers" | Asset type distribution, total count, subcategory breakdown |
| "material" / "grade" queries | Material grade distribution, material diversity |
| "size" queries | Size variety, common sizes, size patterns |
| "manufacturer" queries | Manufacturer distribution, diversity, most common suppliers |
| "asset" / "pipe" / "elbows" queries | Asset type breakdown, subcategory details |
| Multiple aspects | Combine relevant insights, prioritize what user asked about |

**Always include:**
- Total heat number count
- If sample displayed, provide overall statistics for full dataset

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent. **Do not mention "key takeaways" or "insights summary" in the response.**

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence summary answer to the user's specific question from a business perspective.
    * Use total record count as the total count when reporting the volume.
    * If filters applied, mention them in the answer.
    * Examples:
        * "Work order 100500514 has 25 heat numbers across 4 asset types."
        * "Work order 100500514 has 12 Pipe heat numbers with X42 material."

2.  **Key Takeaways:(Do not include any heading like "Key Takeaways" or "Insights Summary" or similar)** Provide targeted insights as separate bullet points following the **TARGETED KEY INSIGHTS** guidelines.
    * Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
    * **CRITICAL FORMAT CONSTRAINT: ALWAYS USE ABSOLUTE COUNTS/NUMBERS ONLY.** **NEVER** use percentages (%), ratios, or fractions for distribution breakdowns.
    * **Focus insights on what user asked about** (material → material insights, size → size insights, etc.).

3.  **Data Request Prompt:** Conclude the response with a single-line prompt asking if they want the full data.
    * Examples: "Would you like to see all heat numbers?", "Need the complete list?", "Should I display the full data?"
    * **CRITICAL**: Never use the word "dataset". **DO NOT** add any other questions or suggestions.

4.  **Table Display:** **STRICTLY DO NOT** display any table in this mode.

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table using phrases like: "show me", "display the data", "yes", "show all", "full data", "full list", or similar.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence confirmation specific to the data being displayed.
    * Example: “Here is the full list of heat numbers for work order 100500514.”

2.  **Key Takeaways:** **STRICTLY DO NOT** include any key takeaways.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt or any other unsolicited questions/suggestions.

4.  **Table Display:** Display the full table with **ALL heat numbers**.
    * **CRITICAL SORTING RULE**: **ALWAYS sort the table by the contents of the first column displayed (ascending order) before rendering the table.**
    * **ALWAYS show core fields:** HeatNumber, Asset, AssetSubcategory.
    * **Add fields based on query keywords** (Material, Size, Manufacturer).
    * **Hide filter parameter fields** that create uniform values.
    * Show ALL rows - no limits.
    * Use clear formatting and handle null values with "-".

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "heat numbers", "records", "data" instead
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**
- **Initial Response (MODE 1): NO TABLE** - just answer + key insights + data request prompt
- **Follow-up Response (MODE 2): FULL TABLE with ALL rows** - no key insights
- Core fields: ALWAYS show HeatNumber, Asset, AssetSubcategory (unless hidden by smart hiding)
- Additional fields: ONLY show when user explicitly mentions them in query
- Filter fields: HIDE if used as filter parameter (creates uniform values)
- WorkOrderNumber: ALWAYS hide (always same - input parameter)
- Key insights: TARGET to match user's query focus

For any counting questions, the total is [X] heat number records. Focus on providing targeted analysis based on what the user asks about, with emphasis on material traceability when relevant.
=== END GetHeatNumberDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
"""