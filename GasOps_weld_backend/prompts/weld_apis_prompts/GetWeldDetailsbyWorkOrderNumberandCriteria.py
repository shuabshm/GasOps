# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetWeldDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     return f"""
# === GetWeldDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API provides detailed weld-level information for specific work orders with rich inspection and material data.

# AVAILABLE FIELDS:
# - Weld identification: WeldSerialNumber, WeldCategory, TieinWeld, Prefab, Gap
# - Material data: HeatSerialNumber1, HeatSerialNumber2, Heat1Description, Heat2Description
# - Welding details: Welder1-4, RootRodClass, FillerRodClass, HotRodClass, CapRodClass
# - Inspection results: CWIName/Result, NDEName/Result/ReportNumber, CRIName/Result, TRName/Result
# - Status indicators: WeldUnlocked, AddedtoWeldMap

# TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY):
# **Show ONLY what the user asks for** - No automatic hierarchy or cascading fields.

# **Inspection Levels:**
# - CWI (visual inspection)
# - NDE inspection
# - CRI inspection
# - TR inspection

# **Field Display Rules:**

# | User Query Pattern | Columns to Display |
# |-------------------|-------------------|
# | **Single inspection level mentioned:** | WeldSerialNumber + ONLY that inspection's fields |
# | "CWI Accept" / "CWI result" | WeldSerialNumber, CWIResult, CWIName |
# | "NDE Reject" / "NDE result" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CRI inspector John" / "CRI result" | WeldSerialNumber, CRIResult, CRIName |
# | "TR result" / "TR inspector" | WeldSerialNumber, TRResult, TRName |
# |  |  |
# | **Multiple inspection levels (both explicitly mentioned):** | WeldSerialNumber + ALL mentioned inspection fields |
# | "CWI Accept and NDE Reject" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber |
# | "NDE and CRI results" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# | "CWI, NDE, and CRI" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# |  |  |
# | **Inspector name queries (include result + name):** | WeldSerialNumber + inspection result + inspector name |
# | "NDE inspector Sam" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CWI inspector Kelly" | WeldSerialNumber, CWIResult, CWIName |
# | "Welds inspected by CRI John" | WeldSerialNumber, CRIResult, CRIName |
# |  |  |
# | **No inspection mentioned:** | WeldSerialNumber only (basic identifier) |
# | "Show all welds" | WeldSerialNumber |
# | "List welds" | WeldSerialNumber |
# |  |  |
# | **Other fields only (no inspection):** | WeldSerialNumber + specific fields asked |
# | "Welds with gaps" | WeldSerialNumber, Gap |
# | "Tie-in welds" | WeldSerialNumber, TieinWeld |
# | "Welds with heat 123" | WeldSerialNumber, HeatSerialNumber (if values vary) |
# |  |  |
# | **Mixed (inspection + other fields):** | WeldSerialNumber + requested inspection fields + other fields |
# | "Gaps with NDE Reject" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap |
# | "Tie-in welds with CWI Accept" | WeldSerialNumber, CWIResult, CWIName, TieinWeld |

# **CRITICAL RULES:**
# - **NO hierarchy** - Don't show CWI just because user asked for NDE
# - **ONLY show what's requested** - User must explicitly mention both CWI and NDE to see both
# - **Inspector queries include result** - "NDE inspector Sam" shows NDEResult + NDEName
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - **Multiple levels** - Only if user explicitly mentions both/all in query

# SMART FIELD HIDING LOGIC:
# **CRITICAL**: Apply intelligent field hiding to avoid redundancy when filters create uniform values.

# **Field Categories:**
# 1. **Core Identifier** - ALWAYS show: WeldSerialNumber
# 2. **WorkOrderNumber** - NEVER show (always same - in input parameter)
# 3. **Inspection Fields** - ONLY show if user requests that inspection level (see Targeted Display Logic above)
#    - Show inspection fields even if filtered (user explicitly asked for them)
# 4. **WeldCategory** - Only show when user explicitly asks about categories/Production/Repaired/CutOut
# 5. **Other Metadata Fields** - Apply smart hiding:
#    - **HIDE if filter creates uniform values** (e.g., HeatSerialNumber=123 → all rows have "123")
#    - **SHOW if values can vary** (e.g., Gap with different values like 0.25, 0.5, 1.0)
#    - Fields subject to smart hiding: HeatSerialNumber, Material, Asset, AssetSubcategory, Size, Manufacturer, Gap (when all same), TieinWeld (when filtered), Prefab (when filtered), RootRodClass, FillerRodClass, HotRodClass, CapRodClass, Welder fields, WeldUnlocked, AddedtoWeldMap

# **Smart Hiding Examples:**
# - "Show welds with heat number 123 and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber (HIDE HeatSerialNumber - all "123", NO CWI fields)
# - "Show welds with gaps and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap (SHOW Gap if values vary, NO CWI fields)
# - "Show tie-in welds with CRI Accept" → Display: WeldSerialNumber, CRIResult, CRIName (HIDE TieinWeld - all "Yes", NO CWI/NDE fields)

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key takeaways + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - If user says "yes", "show all", "full data", or similar → Display full table with all rows
# - **Skip key takeaways** (already provided in previous message)
# - Just provide one-sentence confirmation and full table

# KEY INSIGHTS GUIDELINES (Targeted):
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **What to include (ONLY for displayed fields - targeted approach):**

# 1. **Always include:**
#    - Total count with context: "There are X welds in total"

# 2. **Inspection field distributions (ONLY if that inspection is displayed):**
#    - **If CWI fields shown:** "CWI Results: 75% Accept (150 welds), 20% Reject (40 welds), 5% In Process (10 welds)"
#    - **If NDE fields shown:** "NDE Results: 60% Accept (120 welds), 30% Reject (60 welds), 10% In Process (20 welds)"
#    - **If CRI fields shown:** "CRI Results: 80% Accept (160 welds), 15% Reject (30 welds), 5% Pending (10 welds)"
#    - **If TR fields shown:** "TR Results: 70% Accept (140 welds), 25% Reject (50 welds), 5% In Process (10 welds)"
#    - **CRITICAL:** Only show distributions for inspection levels that are displayed in the table
#    - **Example:** If only NDE fields shown, only provide NDE distribution (no CWI, CRI, or TR)

# 3. **Pattern analysis (ONLY if multiple inspection levels displayed):**
#    - **If both CWI and NDE shown:** "15 welds passed CWI but failed NDE"
#    - **If both NDE and CRI shown:** "10 welds have mismatched results between NDE and CRI"
#    - **Skip pattern analysis if only one inspection level is displayed**

# 4. **If WeldCategory is displayed:**
#    - Category breakdown: "60% Production welds (120), 30% Repaired (60), 10% Cut Out (20)"

# 5. **If material/heat fields displayed:**
#    - Heat diversity: "Uses 15 different heat numbers across all welds"
#    - Material patterns: "All welds use X42 grade steel" or "Mixed materials: 70% X42 (140 welds), 30% X52 (60 welds)"

# 6. **If welder fields displayed:**
#    - Welder distribution: "Top welders: John Doe 40% (80 welds), Jane Smith 35% (70 welds), Mike Johnson 25% (50 welds)"

# 7. **If other attributes displayed (Gap, TieinWeld, Prefab):**
#    - Distribution: "25% are tie-in welds (50)", "15 welds have gaps ranging from 0.25 to 1.0 inches", "30% are prefab (60)"

# 8. **Final summary line (ONLY if alarming or unusual):**
#    - "40 welds have NDE Reject status and may require immediate attention"
#    - "High rejection rate of 35% across all inspections"
#    - "Unusually high number of welds (25) stuck at CRI Reject stage"

# **Format Requirements:**
# - Each insight as a separate bullet point on its own line
# - Never merge into paragraph
# - Use percentages + absolute counts: "75% Accept (150 welds)"
# - Focus on factual observations, not recommendations
# - Keep concise and self-contained
# - **ONLY state factual observations and statistical insights**
# - **DO NOT include recommendations or action items**

# RESPONSE FORMAT:
# 1. **One-sentence answer** to user's specific question from business perspective (no headings, no extra commentary)
#    - Use total count from data. Example: "There are 17 tie-in welds in work order 100500514."

# 2. **Table Contents** (CONDITIONAL based on context):
#    - **If this is INITIAL response**: **DO NOT display any table**

#    - **If this is FOLLOW-UP requesting full data**: Display full table with all rows:
#      - Apply targeted field display logic (NO hierarchy - only requested fields)
#      - Apply smart field hiding to remove redundant columns
#      - Show ALL rows
#      - Use clear formatting and handle null values with "-"

# 3. **Key Takeaways** (CONDITIONAL - only on initial response):
#    - **Show key takeaways ONLY on initial response**
#    - **Skip key takeaways on follow-up response**
#    - Follow Targeted Key Insights Guidelines above
#    - Each bullet on its own line
#    - **ONLY include distributions for inspection levels that are displayed in table**
#    - Include pattern analysis only if multiple inspection levels displayed

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user and ask if they need the full data
#    - Keep it natural and conversational
#    - Examples: "This is a sample. Would you like to see all records?", "Would you like me to display the complete list?"
#    - **CRITICAL**: Never use the word "dataset" - use "data", "records", "welds", "list" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "welds", "records", "data" instead
# - **NO HIERARCHY** - Apply targeted field display logic (show ONLY requested inspection fields)
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - Always show WeldSerialNumber (core identifier)
# - Always apply smart field hiding to avoid redundancy
# - **On initial response: NO TABLE** - just answer + key takeaways + prompt
# - **On follow-up for full data: FULL TABLE with all rows** + NO key takeaways
# - Key takeaways: ONLY for displayed inspection levels (targeted approach)
# - Key takeaways must be calculated from ALL records
# - Pattern analysis: ONLY if multiple inspection levels displayed
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, use the total record count. Focus on targeted inspection analysis based on user query.
# === END GetWeldDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """


# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetWeldDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     return f"""
# === GetWeldDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API provides detailed weld-level information for specific work orders with rich inspection and material data.

# AVAILABLE FIELDS:
# - Weld identification: WeldSerialNumber, WeldCategory (Production, Repaired, CutOut), TieinWeld, Prefab, Gap
# - Material data: HeatSerialNumber1, HeatSerialNumber2, Heat1Description, Heat2Description
# - Welding details: Welder1-4, RootRodClass, FillerRodClass, HotRodClass, CapRodClass
# - Inspection results: CWIName/Result, NDEName/Result/ReportNumber, CRIName/Result, TRName/Result
# - Status indicators: WeldUnlocked, AddedtoWeldMap

# TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY):
# **Show ONLY what the user asks for** - No automatic hierarchy or cascading fields.

# **Inspection Levels:**
# - CWI (visual inspection)
# - NDE inspection
# - CRI inspection
# - TR inspection

# **Field Display Rules:**

# | User Query Pattern | Columns to Display |
# |-------------------|-------------------|
# | **Single inspection level mentioned:** | WeldSerialNumber + ONLY that inspection's fields |
# | "CWI Accept" / "CWI result" | WeldSerialNumber, CWIResult, CWIName |
# | "NDE Reject" / "NDE result" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CRI inspector John" / "CRI result" | WeldSerialNumber, CRIResult, CRIName |
# | "TR result" / "TR inspector" | WeldSerialNumber, TRResult, TRName |
# |  |  |
# | **Multiple inspection levels (both explicitly mentioned):** | WeldSerialNumber + ALL mentioned inspection fields |
# | "CWI Accept and NDE Reject" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber |
# | "NDE and CRI results" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# | "CWI, NDE, and CRI" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# |  |  |
# | **Inspector name queries (include result + name):** | WeldSerialNumber + inspection result + inspector name |
# | "NDE inspector Sam" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CWI inspector Kelly" | WeldSerialNumber, CWIResult, CWIName |
# | "Welds inspected by CRI John" | WeldSerialNumber, CRIResult, CRIName |
# |  |  |
# | **No inspection mentioned:** | WeldSerialNumber only (basic identifier) |
# | "Show all welds" | WeldSerialNumber |
# | "List welds" | WeldSerialNumber |
# |  |  |
# | **Other fields only (no inspection):** | WeldSerialNumber + specific fields asked |
# | "Welds with gaps" | WeldSerialNumber, Gap |
# | "Tie-in welds" | WeldSerialNumber, TieinWeld |
# | "Welds with heat 123" | WeldSerialNumber, HeatSerialNumber (if values vary) |
# |  |  |
# | **Mixed (inspection + other fields):** | WeldSerialNumber + requested inspection fields + other fields |
# | "Gaps with NDE Reject" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap |
# | "Tie-in welds with CWI Accept" | WeldSerialNumber, CWIResult, CWIName, TieinWeld |

# **CRITICAL RULES:**
# - **NO hierarchy** - Don't show CWI just because user asked for NDE
# - **ONLY show what's requested** - User must explicitly mention both CWI and NDE to see both
# - **Inspector queries include result** - "NDE inspector Sam" shows NDEResult + NDEName
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - **Multiple levels** - Only if user explicitly mentions both/all in query
# - **CRITICAL Content Filter Evasion:** The parameter name is **CutOut**, which means a weld has been permanently removed/decommissioned. **When generating conversational text (Step 1 and Step 3), ALWAYS use the term "Removed" or "Decommissioned" instead of "Cut Out" to describe the WeldCategory status to avoid triggering the content filter.**

# SMART FIELD HIDING LOGIC:
# **CRITICAL**: Apply intelligent field hiding to avoid redundancy when filters create uniform values.

# **Field Categories:**
# 1. **Core Identifier** - ALWAYS show: WeldSerialNumber
# 2. **WorkOrderNumber** - NEVER show (always same - in input parameter)
# 3. **Inspection Fields** - ONLY show if user requests that inspection level (see Targeted Display Logic above)
#    - Show inspection fields even if filtered (user explicitly asked for them)
# 4. **WeldCategory** - Only show when user explicitly asks about categories/Production/Repaired/CutOut
# 5. **Other Metadata Fields** - Apply smart hiding:
#    - **HIDE if filter creates uniform values** (e.g., HeatSerialNumber=123 → all rows have "123")
#    - **SHOW if values can vary** (e.g., Gap with different values like 0.25, 0.5, 1.0)
#    - Fields subject to smart hiding: HeatSerialNumber, Material, Asset, AssetSubcategory, Size, Manufacturer, Gap (when all same), TieinWeld (when filtered), Prefab (when filtered), RootRodClass, FillerRodClass, HotRodClass, CapRodClass, Welder fields, WeldUnlocked, AddedtoWeldMap

# **Smart Hiding Examples:**
# - "Show welds with heat number 123 and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber (HIDE HeatSerialNumber - all "123", NO CWI fields)
# - "Show welds with gaps and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap (SHOW Gap if values vary, NO CWI fields)
# - "Show tie-in welds with CRI Accept" → Display: WeldSerialNumber, CRIResult, CRIName (HIDE TieinWeld - all "Yes", NO CWI/NDE fields)
# - "Give me detials of the weld number 251984" → Display the inpsections in a table, NDE Report Film details in a table

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key takeaways + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - If user says "yes", "show all", "full data", or similar → Display full table with all rows
# - **Skip key takeaways** (already provided in previous message)
# - Just provide one-sentence confirmation and full table

# KEY INSIGHTS GUIDELINES (Targeted):
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **What to include (ONLY for displayed fields - targeted approach):**

# 1. **Always include:**
#    - Total count with context: "There are X welds in total"

# 2. **Inspection field distributions (ONLY if that inspection is displayed):**
#    - **If CWI fields shown:** "CWI Results: Accept (150 welds), Reject (40 welds), In Process (10 welds)"
#    - **If NDE fields shown:** "NDE Results: Accept (120 welds), Reject (60 welds), Pending (20 welds)"
#    - **If CRI fields shown:** "CRI Results: Accept (160 welds), Reject (30 welds), Pending (10 welds)"
#    - **If TR fields shown:** "TR Results: Accept (140 welds), Reject (50 welds), In Process (10 welds)"
#    - **CRITICAL:** Only show distributions for inspection levels that are displayed in the table
#    - **Example:** If only NDE fields shown, only provide NDE distribution (no CWI, CRI, or TR)

# 3. **Pattern analysis (ONLY if multiple inspection levels displayed):**
#    - **If both CWI and NDE shown:** "15 welds passed CWI but failed NDE"
#    - **If both NDE and CRI shown:** "10 welds have mismatched results between NDE and CRI"
#    - **Skip pattern analysis if only one inspection level is displayed**

# 4. **If WeldCategory is displayed:**
#    - Category breakdown: "Production welds (120), Repaired (60), Removed (20)"
#     - **Note:** The conversational term **"Removed"** MUST be used here, even though the source field is 'CutOut'.

# 5. **If material/heat fields displayed:**
#    - Heat diversity: "Uses 15 different heat numbers across all welds"
#    - Material patterns: "All welds use X42 grade steel" or "Mixed materials: X42 (140 welds), X52 (60 welds)"

# 6. **If welder fields displayed:**
#    - Welder distribution: "Top welders: John Doe (80 welds), Jane Smith (70 welds), Mike Johnson (50 welds)"

# 7. **If other attributes displayed (Gap, TieinWeld, Prefab):**
#    - Distribution: "Tie-in welds (50)", "15 welds have gaps ranging from 0.25 to 1.0 inches", "Prefab (60)"

# 8. **Final summary line (ONLY if alarming or unusual):**
#    - "40 welds have NDE Reject status and may require immediate attention"
#    - "High rejection rate of 35% across all inspections"
#    - "Unusually high number of welds (25) stuck at CRI Reject stage"

# **Format Requirements:**
# - Each insight as a separate bullet point on its own line
# - Never merge into paragraph
# - Absolute counts: "Accept (150 welds)"
# - Focus on factual observations, not recommendations
# - Keep concise and self-contained
# - **ONLY state factual observations and statistical insights**
# - **DO NOT include recommendations or action items**

# RESPONSE FORMAT:
# 1. **One-sentence answer** to user's specific question from business perspective (no headings, no extra commentary)
#    - Use total count from data. Example: "There are 17 tie-in welds in work order 100500514."

# 2. **Table Contents** (CONDITIONAL based on context):
#    - **If this is INITIAL response**: **DO NOT display any table**

#    - **If this is FOLLOW-UP requesting full data**: Display full table with all rows:
#      - Apply targeted field display logic (NO hierarchy - only requested fields)
#      - Apply smart field hiding to remove redundant columns
#      - Show ALL rows
#      - Use clear formatting and handle null values with "-"

# 3. **Key Takeaways** (CONDITIONAL - only on initial response):
#    - **Show key takeaways ONLY on initial response**
#    - **Skip key takeaways on follow-up response**
#    - Follow Targeted Key Insights Guidelines above
#    - Each bullet on its own line
#    - Do not include any headings like Key takeaways or Summaries.
#    - **ONLY include absolute count for inspection levels that are displayed in table**
#    - Include pattern analysis only if multiple inspection levels displayed

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user and ask if they need the full data
#    - Keep it natural and conversational
#    - Examples: "This is a sample. Would you like to see all records?", "Would you like me to display the complete list?"
#    - **CRITICAL**: Never use the word "dataset" - use "data", "records", "welds", "list" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "welds", "records", "data" instead
# - **NO HIERARCHY** - Apply targeted field display logic (show ONLY requested inspection fields)
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - Always show WeldSerialNumber (core identifier)
# - Always apply smart field hiding to avoid redundancy
# - **On initial response: NO TABLE** - just answer + key takeaways + prompt
# - **On follow-up for full data: FULL TABLE with all rows** + NO key takeaways
# - Key takeaways: ONLY for displayed inspection levels (targeted approach)
# - Key takeaways must be calculated from ALL records
# - Pattern analysis: ONLY if multiple inspection levels displayed
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, use the total record count. Focus on targeted inspection analysis based on user query.
# === END GetWeldDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """





# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetWeldDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     return f"""
# === GetWeldDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

# This API provides detailed weld-level information for specific work orders with rich inspection and material data.

# AVAILABLE FIELDS:
# - Weld identification: WeldSerialNumber, WeldCategory, TieinWeld, Prefab, Gap
# - Material data: HeatSerialNumber1, HeatSerialNumber2, Heat1Description, Heat2Description
# - Welding details: Welder1-4, RootRodClass, FillerRodClass, HotRodClass, CapRodClass
# - Inspection results: CWIName/Result, NDEName/Result/ReportNumber, CRIName/Result, TRName/Result
# - Status indicators: WeldUnlocked, AddedtoWeldMap

# TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY):
# **Show ONLY what the user asks for** - No automatic hierarchy or cascading fields.

# **Inspection Levels:**
# - CWI (visual inspection)
# - NDE inspection
# - CRI inspection
# - TR inspection

# **Field Display Rules:**

# | User Query Pattern | Columns to Display |
# |-------------------|-------------------|
# | **Single inspection level mentioned:** | WeldSerialNumber + ONLY that inspection's fields |
# | "CWI Accept" / "CWI result" | WeldSerialNumber, CWIResult, CWIName |
# | "NDE Reject" / "NDE result" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CRI inspector John" / "CRI result" | WeldSerialNumber, CRIResult, CRIName |
# | "TR result" / "TR inspector" | WeldSerialNumber, TRResult, TRName |
# |  |  |
# | **Multiple inspection levels (both explicitly mentioned):** | WeldSerialNumber + ALL mentioned inspection fields |
# | "CWI Accept and NDE Reject" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber |
# | "NDE and CRI results" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# | "CWI, NDE, and CRI" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# |  |  |
# | **Inspector name queries (include result + name):** | WeldSerialNumber + inspection result + inspector name |
# | "NDE inspector Sam" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CWI inspector Kelly" | WeldSerialNumber, CWIResult, CWIName |
# | "Welds inspected by CRI John" | WeldSerialNumber, CRIResult, CRIName |
# |  |  |
# | **No inspection mentioned:** | WeldSerialNumber only (basic identifier) |
# | "Show all welds" | WeldSerialNumber |
# | "List welds" | WeldSerialNumber |
# |  |  |
# | **Other fields only (no inspection):** | WeldSerialNumber + specific fields asked |
# | "Welds with gaps" | WeldSerialNumber, Gap |
# | "Tie-in welds" | WeldSerialNumber, TieinWeld |
# | "Welds with heat 123" | WeldSerialNumber, HeatSerialNumber (if values vary) |
# |  |  |
# | **Mixed (inspection + other fields):** | WeldSerialNumber + requested inspection fields + other fields |
# | "Gaps with NDE Reject" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap |
# | "Tie-in welds with CWI Accept" | WeldSerialNumber, CWIResult, CWIName, TieinWeld |

# **CRITICAL RULES:**
# - **NO hierarchy** - Don't show CWI just because user asked for NDE
# - **ONLY show what's requested** - User must explicitly mention both CWI and NDE to see both
# - **Inspector queries include result** - "NDE inspector Sam" shows NDEResult + NDEName
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - **Multiple levels** - Only if user explicitly mentions both/all in query

# SMART FIELD HIDING LOGIC:
# **CRITICAL**: Apply intelligent field hiding to avoid redundancy when filters create uniform values.

# **Field Categories:**
# 1. **Core Identifier** - ALWAYS show: WeldSerialNumber
# 2. **WorkOrderNumber** - NEVER show (always same - in input parameter)
# 3. **Inspection Fields** - ONLY show if user requests that inspection level (see Targeted Display Logic above)
#    - Show inspection fields even if filtered (user explicitly asked for them)
# 4. **WeldCategory** - Only show when user explicitly asks about categories/Production/Repaired/CutOut
# 5. **Other Metadata Fields** - Apply smart hiding:
#    - **HIDE if filter creates uniform values** (e.g., HeatSerialNumber=123 → all rows have "123")
#    - **SHOW if values can vary** (e.g., Gap with different values like 0.25, 0.5, 1.0)
#    - Fields subject to smart hiding: HeatSerialNumber, Material, Asset, AssetSubcategory, Size, Manufacturer, Gap (when all same), TieinWeld (when filtered), Prefab (when filtered), RootRodClass, FillerRodClass, HotRodClass, CapRodClass, Welder fields, WeldUnlocked, AddedtoWeldMap

# **Smart Hiding Examples:**
# - "Show welds with heat number 123 and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber (HIDE HeatSerialNumber - all "123", NO CWI fields)
# - "Show welds with gaps and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap (SHOW Gap if values vary, NO CWI fields)
# - "Show tie-in welds with CRI Accept" → Display: WeldSerialNumber, CRIResult, CRIName (HIDE TieinWeld - all "Yes", NO CWI/NDE fields)


# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key takeaways + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - If user says "yes", "show all", "full data", or similar → Display full table with all rows
# - **Skip key takeaways** (already provided in previous message)
# - Just provide one-sentence confirmation and full table

# KEY INSIGHTS GUIDELINES (Targeted):
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **What to include (ONLY for displayed fields - targeted approach):**

# 1. **Always include:**
#    - Total count with context: "There are X welds in total"

# 2. **Inspection field distributions (ONLY if that inspection is displayed):**
#    - **If CWI fields shown:** "CWI Results: 75% Accept (150 welds), 20% Reject (40 welds), 5% In Process (10 welds)"
#    - **If NDE fields shown:** "NDE Results: 60% Accept (120 welds), 30% Reject (60 welds), 10% In Process (20 welds)"
#    - **If CRI fields shown:** "CRI Results: 80% Accept (160 welds), 15% Reject (30 welds), 5% Pending (10 welds)"
#    - **If TR fields shown:** "TR Results: 70% Accept (140 welds), 25% Reject (50 welds), 5% In Process (10 welds)"
#    - **CRITICAL:** Only show distributions for inspection levels that are displayed in the table
#    - **Example:** If only NDE fields shown, only provide NDE distribution (no CWI, CRI, or TR)

# 3. **Pattern analysis (ONLY if multiple inspection levels displayed):**
#    - **If both CWI and NDE shown:** "15 welds passed CWI but failed NDE"
#    - **If both NDE and CRI shown:** "10 welds have mismatched results between NDE and CRI"
#    - **Skip pattern analysis if only one inspection level is displayed**

# 4. **If WeldCategory is displayed:**
#    - Category breakdown: "60% Production welds (120), 30% Repaired (60), 10% Cut Out (20)"

# 5. **If material/heat fields displayed:**
#    - Heat diversity: "Uses 15 different heat numbers across all welds"
#    - Material patterns: "All welds use X42 grade steel" or "Mixed materials: 70% X42 (140 welds), 30% X52 (60 welds)"

# 6. **If welder fields displayed:**
#    - Welder distribution: "Top welders: John Doe 40% (80 welds), Jane Smith 35% (70 welds), Mike Johnson 25% (50 welds)"

# 7. **If other attributes displayed (Gap, TieinWeld, Prefab):**
#    - Distribution: "25% are tie-in welds (50)", "15 welds have gaps ranging from 0.25 to 1.0 inches", "30% are prefab (60)"

# 8. **Final summary line (ONLY if alarming or unusual):**
#    - "40 welds have NDE Reject status and may require immediate attention"
#    - "High rejection rate of 35% across all inspections"
#    - "Unusually high number of welds (25) stuck at CRI Reject stage"

# **Format Requirements:**
# - Each insight as a separate bullet point on its own line
# - Never merge into paragraph
# - Use percentages + absolute counts: "75% Accept (150 welds)"
# - Focus on factual observations, not recommendations
# - Keep concise and self-contained
# - **ONLY state factual observations and statistical insights**
# - **DO NOT include recommendations or action items**

# RESPONSE FORMAT:
# 1. **One-sentence answer** to user's specific question from business perspective (no headings, no extra commentary)
#    - Use total count from data. Example: "There are 17 tie-in welds in work order 100500514."

# 2. **Table Contents** (CONDITIONAL based on context):
#    - **If this is INITIAL response**: **DO NOT display any table**

#    - **If this is FOLLOW-UP requesting full data**: Display full table with all rows:
#      - Apply targeted field display logic (NO hierarchy - only requested fields)
#      - Apply smart field hiding to remove redundant columns
#      - Show ALL rows
#      - Use clear formatting and handle null values with "-"

# 3. **Key Takeaways** (CONDITIONAL - only on initial response):
#    - **Show key takeaways ONLY on initial response**
#    - **Skip key takeaways on follow-up response**
#    - Follow Targeted Key Insights Guidelines above
#    - Each bullet on its own line
#    - **ONLY include distributions for inspection levels that are displayed in table**
#    - Include pattern analysis only if multiple inspection levels displayed

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user and ask if they need the full data
#    - Keep it natural and conversational
#    - Examples: "This is a sample. Would you like to see all records?", "Would you like me to display the complete list?"
#    - **CRITICAL**: Never use the word "dataset" - use "data", "records", "welds", "list" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "welds", "records", "data" instead
# - **NO HIERARCHY** - Apply targeted field display logic (show ONLY requested inspection fields)
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - Always show WeldSerialNumber (core identifier)
# - Always apply smart field hiding to avoid redundancy
# - **On initial response: NO TABLE** - just answer + key takeaways + prompt
# - **On follow-up for full data: FULL TABLE with all rows** + NO key takeaways
# - Key takeaways: ONLY for displayed inspection levels (targeted approach)
# - Key takeaways must be calculated from ALL records
# - Pattern analysis: ONLY if multiple inspection levels displayed
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, use the total record count. Focus on targeted inspection analysis based on user query.
# === END GetWeldDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """


# This API provides detailed weld-level information for specific work orders with rich inspection and material data.

# AVAILABLE FIELDS:
# - Weld identification: WeldSerialNumber, WeldCategory (Production, Repaired, CutOut), TieinWeld, Prefab, Gap
# - Material data: HeatSerialNumber1, HeatSerialNumber2, Heat1Description, Heat2Description
# - Welding details: Welder1-4, RootRodClass, FillerRodClass, HotRodClass, CapRodClass
# - Inspection results: CWIName/Result, NDEName/Result/ReportNumber, CRIName/Result, TRName/Result
# - Status indicators: WeldUnlocked, AddedtoWeldMap

# TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY):
# **Show ONLY what the user asks for** - No automatic hierarchy or cascading fields.

# **Inspection Levels:**
# - CWI (visual inspection)
# - NDE inspection
# - CRI inspection
# - TR inspection

# **Field Display Rules:**

# | User Query Pattern | Columns to Display |
# |-------------------|-------------------|
# | **Single inspection level mentioned:** | WeldSerialNumber + ONLY that inspection's fields |
# | "CWI Accept" / "CWI result" | WeldSerialNumber, CWIResult, CWIName |
# | "NDE Reject" / "NDE result" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CRI inspector John" / "CRI result" | WeldSerialNumber, CRIResult, CRIName |
# | "TR result" / "TR inspector" | WeldSerialNumber, TRResult, TRName |
# |  |  |
# | **Multiple inspection levels (both explicitly mentioned):** | WeldSerialNumber + ALL mentioned inspection fields |
# | "CWI Accept and NDE Reject" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber |
# | "NDE and CRI results" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# | "CWI, NDE, and CRI" | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# |  |  |
# | **Inspector name queries (include result + name):** | WeldSerialNumber + inspection result + inspector name |
# | "NDE inspector Sam" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber |
# | "CWI inspector Kelly" | WeldSerialNumber, CWIResult, CWIName |
# | "Welds inspected by CRI John" | WeldSerialNumber, CRIResult, CRIName |
# |  |  |
# | **No inspection mentioned:** | WeldSerialNumber only (basic identifier) |
# | "Show all welds" | WeldSerialNumber |
# | "List welds" | WeldSerialNumber |
# |  |  |
# | **Other fields only (no inspection):** | WeldSerialNumber + specific fields asked |
# | "Welds with gaps" | WeldSerialNumber, Gap |
# | "Tie-in welds" | WeldSerialNumber, TieinWeld |
# | "Welds with heat 123" | WeldSerialNumber, HeatSerialNumber (if values vary) |
# |  |  |
# | **Mixed (inspection + other fields):** | WeldSerialNumber + requested inspection fields + other fields |
# | "Gaps with NDE Reject" | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap |
# | "Tie-in welds with CWI Accept" | WeldSerialNumber, CWIResult, CWIName, TieinWeld |

# **CRITICAL RULES:**
# - **NO hierarchy** - Don't show CWI just because user asked for NDE
# - **ONLY show what's requested** - User must explicitly mention both CWI and NDE to see both
# - **Inspector queries include result** - "NDE inspector Sam" shows NDEResult + NDEName
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - **Multiple levels** - Only if user explicitly mentions both/all in query
# - **CRITICAL Content Filter Evasion:** The parameter name is **CutOut**, which means a weld has been permanently removed/decommissioned. **When generating conversational text (Step 1 and Step 3), ALWAYS use the term "Removed" or "Decommissioned" instead of "Cut Out" to describe the WeldCategory status to avoid triggering the content filter.**

# SMART FIELD HIDING LOGIC:
# **CRITICAL**: Apply intelligent field hiding to avoid redundancy when filters create uniform values.

# **Field Categories:**
# 1. **Core Identifier** - ALWAYS show: WeldSerialNumber
# 2. **WorkOrderNumber** - NEVER show (always same - in input parameter)
# 3. **Inspection Fields** - ONLY show if user requests that inspection level (see Targeted Display Logic above)
#    - Show inspection fields even if filtered (user explicitly asked for them)
# 4. **WeldCategory** - Only show when user explicitly asks about categories/Production/Repaired/CutOut
# 5. **Other Metadata Fields** - Apply smart hiding:
#    - **HIDE if filter creates uniform values** (e.g., HeatSerialNumber=123 → all rows have "123")
#    - **SHOW if values can vary** (e.g., Gap with different values like 0.25, 0.5, 1.0)
#    - Fields subject to smart hiding: HeatSerialNumber, Material, Asset, AssetSubcategory, Size, Manufacturer, Gap (when all same), TieinWeld (when filtered), Prefab (when filtered), RootRodClass, FillerRodClass, HotRodClass, CapRodClass, Welder fields, WeldUnlocked, AddedtoWeldMap

# **Smart Hiding Examples:**
# - "Show welds with heat number 123 and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber (HIDE HeatSerialNumber - all "123", NO CWI fields)
# - "Show welds with gaps and NDE Reject" → Display: WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap (SHOW Gap if values vary, NO CWI fields)
# - "Show tie-in welds with CRI Accept" → Display: WeldSerialNumber, CRIResult, CRIName (HIDE TieinWeld - all "Yes", NO CWI/NDE fields)
# - "Give me detials of the weld number 251984" → Display the inpsections in a table, NDE Report Film details in a table

# RESPONSE FLOW:

# **Initial Response:**
# - Provide one-sentence answer + key takeaways + data request prompt
# - **DO NOT display any table**

# **Follow-up Response (when user requests full data):**
# - If user says "yes", "show all", "full data", or similar → Display full table with all rows
# - **Skip key takeaways** (already provided in previous message)
# - Just provide one-sentence confirmation and full table

# KEY INSIGHTS GUIDELINES (Targeted):
# **When to show:**
# - Show on initial query response
# - Skip on follow-up when user requests full data

# **What to include (ONLY for displayed fields - targeted approach):**

# 1. **Always include:**
#    - Total count with context: "There are X welds in total"
#    - Avoid restating the same status in bullet points if the result distribution is uniform (e.g., all Accept or all Reject).

# 2. **Inspection field distributions (ONLY if that inspection is displayed):**
#    - **If CWI fields shown:** "CWI Results: Accept (150 welds), Reject (40 welds), In Process (10 welds)"
#    - **If NDE fields shown:** "NDE Results: Accept (120 welds), Reject (60 welds), Pending (20 welds)"
#    - **If CRI fields shown:** "CRI Results: Accept (160 welds), Reject (30 welds), Pending (10 welds)"
#    - **If TR fields shown:** "TR Results: Accept (140 welds), Reject (50 welds), In Process (10 welds)"
#    - **CRITICAL:** Only show distributions for inspection levels that are displayed in the table
#    - **Example:** If only NDE fields shown, only provide NDE distribution (no CWI, CRI, or TR)
#    - Skip distribution bullet entirely if all welds share the same result (e.g., all Accept).

# 3. **Pattern analysis (ONLY if multiple inspection levels displayed):**
#    - **If both CWI and NDE shown:** "15 welds passed CWI but failed NDE"
#    - **If both NDE and CRI shown:** "10 welds have mismatched results between NDE and CRI"
#    - **Skip pattern analysis if only one inspection level is displayed**

# 4. **If WeldCategory is displayed:**
#    - Category breakdown: "Production welds (120), Repaired (60), Removed (20)"
#     - **Note:** The conversational term **"Removed"** MUST be used here, even though the source field is 'CutOut'.

# 5. **If material/heat fields displayed:**
#    - Heat diversity: "Uses 15 different heat numbers across all welds"
#    - Material patterns: "All welds use X42 grade steel" or "Mixed materials: X42 (140 welds), X52 (60 welds)"

# 6. **If welder fields displayed:**
#    - Welder distribution: "Top welders: John Doe (80 welds), Jane Smith (70 welds), Mike Johnson (50 welds)"

# 7. **If other attributes displayed (Gap, TieinWeld, Prefab):**
#    - Distribution: "Tie-in welds (50)", "15 welds have gaps ranging from 0.25 to 1.0 inches", "Prefab (60)"

# 8. **Final summary line (ONLY if alarming or unusual):**
#    - "40 welds have NDE Reject status and may require immediate attention"
#    - "High rejection rate of 35% across all inspections"
#    - "Unusually high number of welds (25) stuck at CRI Reject stage"

# **Format Requirements:**
# - Each insight as a separate bullet point on its own line
# - Never merge into paragraph
# - Absolute counts: "Accept (150 welds)"
# - Dont use percentages (%)
# - Focus on factual observations, not recommendations
# - Keep concise and self-contained
# - **ONLY state factual observations and statistical insights**
# - **DO NOT include recommendations or action items**

# RESPONSE FORMAT:
# 1. **One-sentence answer** to user's specific question from business perspective (no headings, no extra commentary)
#    - Use total count from data. Example: "There are 17 tie-in welds in work order 100500514."
#    - Exception for weld-number-only queries:
#         - **If the query explicitly asks only for weld numbers (e.g., “List the weld numbers”, “Show weld numbers for work order…”), then:
#             - Return a single sentence stating the weld numbers separated by commas.
#             - Make sure to include the count of welds.
#             - Do not display any table, key takeaways, or follow-up prompts.**

# 2. **Table Contents** (CONDITIONAL based on context):
#    - **If this is INITIAL response**: **DO NOT display any table**

#    - **If this is FOLLOW-UP requesting full data**: Display full table with all rows:
#      - Apply targeted field display logic (NO hierarchy - only requested fields)
#      - Apply smart field hiding to remove redundant columns
#      - Show ALL rows
#      - Use clear formatting and handle null values with "-"

# 3. **Key Takeaways** (CONDITIONAL - only on initial response):
#    - **Show key takeaways ONLY on initial response**
#    - **Skip key takeaways on follow-up response**
#    - Follow Targeted Key Insights Guidelines above
#    - Each bullet on its own line
#    - Do not include any headings like Key takeaways or Summaries.
#    - **ONLY include absolute count for inspection levels that are displayed in table**
#    - Include pattern analysis only if multiple inspection levels displayed

# 4. **Data Request Prompt** (only on initial response):
#    - Inform the user and ask if they need the full data
#    - Keep it natural and conversational
#    - Examples: "This is a sample. Would you like to see all records?", "Would you like me to display the complete list?"
#    - **CRITICAL**: Never use the word "dataset" - use "data", "records", "welds", "list" instead
#    - **DO NOT** add any other questions, suggestions, or offers for additional analysis

# CRITICAL RULES:
# - **NEVER use the word "dataset"** - use "welds", "records", "data" instead
# - **NO HIERARCHY** - Apply targeted field display logic (show ONLY requested inspection fields)
# - **WorkOrderNumber is NEVER shown** - Always same (in input parameter)
# - Always show WeldSerialNumber (core identifier)
# - Always apply smart field hiding to avoid redundancy
# - **On initial response: NO TABLE** - just answer + key takeaways + prompt
# - **On follow-up for full data: FULL TABLE with all rows** + NO key takeaways
# - Key takeaways: ONLY for displayed inspection levels (targeted approach)
# - Key takeaways must be calculated from ALL records
# - Pattern analysis: ONLY if multiple inspection levels displayed
# - **NEVER add unsolicited follow-up questions or suggestions**
# - **ONLY answer what was asked**

# For any counting questions, use the total record count. Focus on targeted inspection analysis based on user query.










# def get_api_prompt(api_parameters=None):
#     """
#     Returns the API-specific prompt for GetWeldDetailsbyWorkOrderNumberandCriteria API

#     Args:
#         api_parameters (dict): Optional dictionary of API filter parameters

#     Returns:
#         str: The formatted API-specific prompt
#     """
#     return f"""
# === GetWeldDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
# **IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**
# This API provides detailed weld-level information for specific work orders with rich inspection and material data.

# AVAILABLE FIELDS
#     - Weld identification: WeldSerialNumber, WeldCategory (Production, Repaired, CutOut), TieinWeld, Prefab, Gap
#     - Material data: HeatSerialNumber1, HeatSerialNumber2, Heat1Description, Heat2Description
#     - Welding details: Welder1–4, RootRodClass, FillerRodClass, HotRodClass, CapRodClass
#     - Inspection results: CWIName/Result, NDEName/Result/ReportNumber, CRIName/Result, TRName/Result
#     - Status indicators: WeldUnlocked, AddedtoWeldMap

# **CRITICAL WELD NUMBER PATTERN RECOGNITION:**
# - **Any WeldSerialNumber ending with "-R" (e.g., 240252-R, 250303-R) is a REPAIRED weld**
# - This suffix indicates the weld has been repaired/reworked
# - When counting or categorizing welds:
#   - If WeldSerialNumber ends with "-R", treat it as WeldCategory = "Repaired"
#   - This applies even if the WeldCategory field shows something different
#   - Examples: "240252-R", "250292-R", "250303-R", "250307-R" are all repaired welds
# - When filtering by WeldCategory="Repaired", include both:
#   - Welds where WeldCategory field = "Repaired"
#   - Welds where WeldSerialNumber ends with "-R"

# TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY)
# **Show ONLY what the user asks for** — no automatic hierarchy or cascading fields.

# Inspection Levels:
#     - CWI (visual inspection)
#     - NDE inspection
#     - CRI inspection
#     - TR inspection

# | User Query Pattern                                    | Columns to Display                                                                            |
# | ----------------------------------------------------- | --------------------------------------------------------------------------------------------- |
# | **Single inspection level mentioned:**                | WeldSerialNumber + ONLY that inspection’s fields                                              |
# | “CWI Accept” / “CWI result”                           | WeldSerialNumber, CWIResult, CWIName                                                          |
# | “NDE Reject” / “NDE result”                           | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber                                         |
# | “CRI inspector John” / “CRI result”                   | WeldSerialNumber, CRIResult, CRIName                                                          |
# | “TR result” / “TR inspector”                          | WeldSerialNumber, TRResult, TRName                                                            |
# | **Multiple inspection levels mentioned:**             | WeldSerialNumber + all explicitly mentioned inspection fields                                 |
# | “CWI Accept and NDE Reject”                           | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber                     |
# | “NDE and CRI results”                                 | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName                     |
# | “CWI, NDE, and CRI”                                   | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
# | **Inspector name queries:**                           | WeldSerialNumber + inspection result + inspector name                                         |
# | “NDE inspector Sam”                                   | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber                                         |
# | “CWI inspector Kelly”                                 | WeldSerialNumber, CWIResult, CWIName                                                          |
# | “Welds inspected by CRI John”                         | WeldSerialNumber, CRIResult, CRIName                                                          |
# | **No inspection mentioned (basic weld list):**        | WeldSerialNumber only                                                                         |
# | “Show all welds” / “List welds” / “Show me the welds” | WeldSerialNumber only                                                                         |
# | **Other fields only (no inspection):**                | WeldSerialNumber + specifically requested fields                                              |
# | “Welds with gaps”                                     | WeldSerialNumber, Gap                                                                         |
# | “Tie-in welds”                                        | WeldSerialNumber, TieinWeld                                                                   |
# | “Welds with heat 123”                                 | WeldSerialNumber, HeatSerialNumber (if values vary)                                           |
# | **Mixed (inspection + other fields):**                | WeldSerialNumber + requested inspection fields + requested other fields                       |
# | “Gaps with NDE Reject”                                | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap                                    |
# | “Tie-in welds with CWI Accept”                        | WeldSerialNumber, CWIResult, CWIName, TieinWeld                                               |



# CRITICAL RULES
# - **NO hierarchy**: Don’t show CWI just because user asked for NDE.
# - **ONLY show what’s requested.**
# - **Inspector queries include result.**
# - **WorkOrderNumber is NEVER shown.**
# - **Multiple levels only if explicitly mentioned.**
# - **Content Filter Rule**: When referencing CutOut, always use “Removed” or “Decommissioned” in text responses.

# SMART FIELD HIDING LOGIC
# Apply intelligent field hiding to avoid redundancy when filters create uniform values.
#     1.Core Identifier: Always show WeldSerialNumber
#     2.WorkOrderNumber: Never show (always same)
#     3.Inspection Fields: Only show if user requests them
#     4.WeldCategory: Only show if user explicitly asks for categories (Production/Repaired/Removed)
#     5.Other Metadata Fields:
#         - Hide if all values are identical.
#         - Show only if values vary.

# Fields subject to smart hiding: HeatSerialNumber, Material, Asset, AssetSubcategory, Size, Manufacturer, Gap (when all same), TieinWeld (when filtered), Prefab (when filtered), RodClass fields, Welder fields, WeldUnlocked, AddedtoWeldMap

# Examples:
# “Show welds with heat number 123 and NDE Reject” → Hide HeatSerialNumber (all same).
# “Show welds with gaps and NDE Reject” → Show Gap only if variable.
# “Show tie-in welds with CRI Accept” → Hide TieinWeld if all “Yes.”
# “Give me details of weld number 251984” → Show full inspection results in table.

# RESPONSE FLOW

# Initial Response:

# One-sentence answer + key takeaways + data request prompt

# Do NOT display a table

# Follow-up Response:

# If user says “show all,” “yes,” or similar → show full table (do not mention any key takeaways).

# KEY INSIGHTS GUIDELINES (REDUNDANCY-FREE)

# When to show:

# Only on initial response, skip on follow-up.

# Show only for displayed fields.
# If only WeldSerialNumber is shown, skip insights entirely.

# Always include:

# “There are X welds in work order QG21011633.”

# Skip any bullet points if only counts are available.

# Inspection field distributions (only if mixed):

# Example: “NDE Results: Accept (120), Reject (60), Pending (20).”

# Skip entirely if all results are uniform.

# Pattern analysis (only if multiple inspections):

# Example: “15 welds passed CWI but failed NDE.”

# Skip otherwise.

# If WeldCategory shown:

# "Production welds (120), Repaired (60), Removed (20)."

# **IMPORTANT**: When counting Repaired welds, include BOTH:
#   - Welds with WeldCategory = "Repaired"
#   - Welds with WeldSerialNumber ending in "-R"

# If material or heat fields shown:

# “Uses 15 different heat numbers.”

# Skip if only one unique value.

# If welder fields shown:

# “Top welders: John Doe (80), Jane Smith (70).”

# If other attributes shown (Gap, TieinWeld, Prefab):

# Show distribution only if variation exists.

# Skip redundant summaries.

# If total count or uniform status already stated, do not repeat in bullet points.

# RESPONSE FORMAT

# One-Sentence Answer

# Example: “There are 17 tie-in welds in work order 100500514.”

# Exception — Weld Number Queries:

# If the user asks for only weld numbers (e.g., “Show weld numbers for work order…”):

# Respond with a single sentence listing them, separated by commas.

# Include the total count.

# No table, no key takeaways, no follow-up prompt.

# Table (Conditional)

# Only for explicit “show all” or “full data” follow-up.

# Apply smart hiding and targeted display logic.

# Key Takeaways (Conditional)

# Only if fields beyond WeldSerialNumber are displayed.

# Skip for weld-number-only or count-only queries.

# Data Request Prompt (Conditional)

# Only in initial response.

# Example: “Would you like me to display the complete list?”

# Never say “dataset.” Use “data,” “records,” or “welds.”

# CRITICAL BEHAVIOR RULES

# Never show WorkOrderNumber.

# Never infer or add extra fields.

# Never repeat the same insight twice.

# Never show inspection/category/welder info for “show all welds” queries.

# For uniform results (all Accept/Reject), collapse into one clean sentence.

# For counting queries, use total count only once.

# For “show all welds,” display only weld numbers.

# For “show weld numbers,” output only a comma-separated list and distict count.


# === END GetWeldDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
# """







def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetWeldDetailsbyWorkOrderNumberandCriteria API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    return f"""
=== GetWeldDetailsbyWorkOrderNumberandCriteria API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**
This API provides detailed weld-level information for specific work orders with rich inspection and material data.

AVAILABLE FIELDS
    - Weld identification: WeldSerialNumber, WeldCategory (Production, Repaired, CutOut), TieinWeld, Prefab, Gap
    - Material data: HeatSerialNumber1, HeatSerialNumber2, Heat1Description, Heat2Description
    - Welding details: Welder1–4, RootRodClass, FillerRodClass, HotRodClass, CapRodClass
    - Inspection results: CWIName/Result, NDEName/Result/ReportNumber, CRIName/Result, TRName/Result
    - Status indicators: WeldUnlocked, AddedtoWeldMap

**CRITICAL WELD NUMBER PATTERN RECOGNITION:**
- **Any WeldSerialNumber ending with "-R" (e.g., 240252-R, 250303-R) is a REPAIRED weld**
- This suffix indicates the weld has been repaired/reworked
- When counting or categorizing welds:
    - If WeldSerialNumber ends with "-R", treat it as WeldCategory = "Repaired"
    - This applies even if the WeldCategory field shows something different
    - Examples: "240252-R", "250292-R", "250303-R", "250307-R" are all repaired welds
- When filtering by WeldCategory="Repaired", include both:
    - Welds where WeldCategory field = "Repaired"
    - Welds where WeldSerialNumber ends with "-R"

TARGETED FIELD DISPLAY LOGIC (NO HIERARCHY)
**Show ONLY what the user asks for** — no automatic hierarchy or cascading fields.

Inspection Levels:
    - CWI (visual inspection)
    - NDE inspection
    - CRI inspection
    - TR inspection

| User Query Pattern                                    | Columns to Display                                                                            |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Single inspection level mentioned:** | WeldSerialNumber + ONLY that inspection’s fields                                              |
| “CWI Accept” / “CWI result”                           | WeldSerialNumber, CWIResult, CWIName                                                          |
| “NDE Reject” / “NDE result”                           | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber                                         |
| “CRI inspector John” / “CRI result”                   | WeldSerialNumber, CRIResult, CRIName                                                          |
| “TR result” / “TR inspector”                          | WeldSerialNumber, TRResult, TRName                                                            |
| **Multiple inspection levels mentioned:** | WeldSerialNumber + all explicitly mentioned inspection fields                                 |
| “CWI Accept and NDE Reject”                           | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber                     |
| “NDE and CRI results”                                 | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName                     |
| “CWI, NDE, and CRI”                                   | WeldSerialNumber, CWIResult, CWIName, NDEResult, NDEName, NDEReportNumber, CRIResult, CRIName |
| **Inspector name queries:** | WeldSerialNumber + inspection result + inspector name                                         |
| “NDE inspector Sam”                                   | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber                                         |
| “CWI inspector Kelly”                                 | WeldSerialNumber, CWIResult, CWIName                                                          |
| “Welds inspected by CRI John”                         | WeldSerialNumber, CRIResult, CRIName                                                          |
| **No inspection mentioned (basic weld list):** | WeldSerialNumber only                                                                         |
| “Show all welds” / “List welds” / “Show me the welds” | WeldSerialNumber only                                                                         |
| **Other fields only (no inspection):** | WeldSerialNumber + specifically requested fields                                              |
| “Welds with gaps”                                     | WeldSerialNumber, Gap                                                                         |
| “Tie-in welds”                                        | WeldSerialNumber, TieinWeld                                                                   |
| “Welds with heat 123”                                 | WeldSerialNumber, HeatSerialNumber (if values vary)                                           |
| **Mixed (inspection + other fields):** | WeldSerialNumber + requested inspection fields + requested other fields                       |
| “Gaps with NDE Reject”                                | WeldSerialNumber, NDEResult, NDEName, NDEReportNumber, Gap                                    |
| “Tie-in welds with CWI Accept”                        | WeldSerialNumber, CWIResult, CWIName, TieinWeld                                               |


CRITICAL RULES
- **NO hierarchy**: Don’t show CWI just because user asked for NDE.
- **ONLY show what’s requested.**
- **Inspector queries include result.**
- **WorkOrderNumber is NEVER shown.**
- **Multiple levels only if explicitly mentioned.**
- **Content Filter Rule**: When referencing CutOut, always use “Removed” or “Decommissioned” in text responses.

SMART FIELD HIDING LOGIC
Apply intelligent field hiding to avoid redundancy when filters create uniform values.
    1.Core Identifier: Always show WeldSerialNumber
    2.WorkOrderNumber: Never show (always same)
    3.Inspection Fields: Only show if user requests them
    4.WeldCategory: Only show if user explicitly asks for categories (Production/Repaired/Removed)
    5.Other Metadata Fields:
        - Hide if all values are identical.
        - Show only if values vary.

Fields subject to smart hiding: HeatSerialNumber, Material, Asset, AssetSubcategory, Size, Manufacturer, Gap (when all same), TieinWeld (when filtered), Prefab (when filtered), RodClass fields, Welder fields, WeldUnlocked, AddedtoWeldMap

Examples:
“Show welds with heat number 123 and NDE Reject” → Hide HeatSerialNumber (all same).
“Show welds with gaps and NDE Reject” → Show Gap only if variable.
“Show tie-in welds with CRI Accept” → Hide TieinWeld if all “Yes.”
“Give me details of weld number 251984” → Show full inspection results in table.

KEY INSIGHTS GUIDELINES (REDUNDANCY-FREE)

When to show:

Only on initial response, skip on follow-up.

Show only for displayed fields.
If only WeldSerialNumber is shown, skip insights entirely.

Always include:

“There are X welds in work order QG21011633.”

Skip any bullet points if only counts are available.

Inspection field distributions (only if mixed):

Example: “NDE Results: Accept (120), Reject (60), Pending (20).”

Skip entirely if all results are uniform.

Pattern analysis (only if multiple inspections):

Example: “15 welds passed CWI but failed NDE.”

Skip otherwise.

If WeldCategory shown:

"Production welds (120), Repaired (60), Removed (20)."

**IMPORTANT**: When counting Repaired welds, include BOTH:
    - Welds with WeldCategory = "Repaired"
    - Welds with WeldSerialNumber ending in "-R"

If material or heat fields shown:

“Uses 15 different heat numbers.”

Skip if only one unique value.

If welder fields shown:

“Top welders: John Doe (80), Jane Smith (70).”

If other attributes shown (Gap, TieinWeld, Prefab):

Show distribution only if variation exists.

Skip redundant summaries.

If total count or uniform status already stated, do not repeat in bullet points.

**RESPONSE FLOW & FORMATTING RULES**

The response structure is determined by the user's explicit intent.

**MODE 1: INSIGHT MODE (Default for Analysis/Initial Queries)**
This mode applies to any question that asks for analysis, counts, distributions, or is the user's first general query.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence summary answer to the user's question.
    * Example: “There are 17 tie-in welds in work order 100500514.”
    * *Exception:* For weld number queries (e.g., “Show weld numbers”), respond with the comma-separated list and total count only (No Key Takeaways, No Data Request Prompt).

2.  **Key Takeaways (Conditional):** Present relevant **KEY INSIGHTS GUIDELINES** as bullet points *only* if fields beyond `WeldSerialNumber` are displayed. Skip for weld-number-only or count-only queries. **Strictly do not display a table.**

3.  **Data Request Prompt (Conditional):** Always conclude the response with a single-line prompt asking the user if they want the full data in a table.
    * Example: “Would you like me to display the complete list?”

**MODE 2: TABULAR MODE (For Explicit Data Display)**
This mode is triggered ONLY when the user asks explicitly to see the data in a table using phrases like: “show all,” “yes, show the table,” “full data,” “in tabular form,” etc.

1.  **One-Sentence Answer:** Provide a concise, direct, one-sentence answer specific to the data being displayed.
    * Example: “Here are the welds that failed NDE in a structured format.”

2.  **Key Takeaways:** **STRICTLY DO NOT** include the Key Takeaways section.

3.  **Data Request Prompt:** **STRICTLY DO NOT** include a Data Request Prompt.

4.  **Table Display:** Display the final, filtered, sorted table following the **CRITICAL TABLE DISPLAY RULES** and **TARGETED FIELD DISPLAY LOGIC**. Apply smart hiding logic before generation.

CRITICAL BEHAVIOR RULES

Never show WorkOrderNumber.

Never infer or add extra fields.

Never repeat the same insight twice.

Never show inspection/category/welder info for “show all welds” queries.

For uniform results (all Accept/Reject), collapse into one clean sentence.

For counting queries, use total count only once.

For “show all welds,” display only weld numbers.

For “show weld numbers,” output only a comma-separated list and distict count.


=== END GetWeldDetailsbyWorkOrderNumberandCriteria GUIDELINES ===
"""