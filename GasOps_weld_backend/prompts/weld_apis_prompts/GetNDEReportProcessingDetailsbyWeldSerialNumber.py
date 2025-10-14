def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetNDEReportProcessingDetailsbyWeldSerialNumber API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}
    
    return f"""
=== GetNDEReportProcessingDetailsbyWeldSerialNumber API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns detailed NDE report processing information for a specific weld, including technical parameters used in NDE inspection.

RESPONSE STRUCTURE:
The API returns a list of NDE reports with technical processing details.

AVAILABLE FIELDS (Many technical fields available):
- WeldSerialNumber: Weld serial number (required filter parameter - always same for all records)
- NDEReportNumber: NDE report identifier (e.g., "NDE2025-00571 (Conv)")
- NDEName: NDE inspector name (e.g., "Sam Maldonado")
- Technique: NDE technique used (e.g., "DWE/SWV", "RT", "UT")
- Source: Source material/radiation type (e.g., "Ir", "Co-60")
- FilmType: Type of film used (e.g., "AFGA D7")
- ExposureTime: Exposure time in seconds
- ThicknessofWeld: Weld thickness measurement
- CurieStrength: Radiation strength
- FilmSize: Size of film (e.g., "4.5\" x 17\"")
- FilmLoad: Film loading type (Single/Double)
- IQILocation: Image Quality Indicator location (Film Side/Source Side)
- ASTMPackID: ASTM pack identifier
- LeadScreensFront: Front lead screen thickness
- LeadScreensBack: Back lead screen thickness
- Additional fields based on report type (Conventional vs other types)

TARGETED FIELD DISPLAY LOGIC:

**Core Fields (ALWAYS show):**
- NDEReportNumber
- NDEName
- Technique
- Source

**Default Technical Fields (show for general queries):**
- FilmType
- ExposureTime
- ThicknessofWeld

**Additional Fields (ONLY when user explicitly mentions):**

| User Query Pattern | Additional Columns to Display |
|-------------------|------------------------------|
| General "NDE reports" / "processing details" | Core + FilmType, ExposureTime, ThicknessofWeld |
| "film" / "film type" / "film details" | + FilmSize, FilmLoad |
| "exposure" / "exposure time" / "radiation" | + CurieStrength |
| "thickness" / "weld thickness" | ThicknessofWeld (already in default) |
| "lead screens" / "screen" / "lead" | + LeadScreensFront, LeadScreensBack |
| "IQI" / "image quality" / "quality indicator" | + IQILocation |
| "ASTM" / "pack" | + ASTMPackID |
| "all details" / "complete" / "everything" / "all fields" | All available technical fields |

**Smart Field Hiding:**
- **WeldSerialNumber**: ALWAYS hide (required filter parameter - always same for all records)

Field Display Rules:
- Use "-" for null/empty values
- Maintain column ordering: Core fields first, then technical fields (default or requested)
- Use clear column headers
- Handle nested structures by flattening into table columns

RESPONSE FLOW:

**Initial Response:**
- Provide one-sentence answer + key insights + data request prompt
- **DO NOT display any table**

**Follow-up Response (when user requests full data):**
- Display full table with all rows
- **Skip key insights**

TABLE SORTING:
**Default:** NDEReportNumber ascending (chronological order)

TARGETED KEY INSIGHTS:
**When to show:**
- Show on initial query response
- Skip on follow-up when user requests full data

**Match insights focus to what user asked about:**

| User Query Focus | Key Insights To Provide |
|-----------------|------------------------|
| General "NDE reports" | Report count, report type distribution, inspector assignments, key technical parameters summary |
| "film" queries | Film types used, film sizes, film load patterns |
| "exposure" queries | Exposure time range, source types, curie strength variations |
| "thickness" queries | Weld thickness measurements, thickness variations |
| "lead screens" queries | Lead screen configurations, front/back thickness patterns |
| Technical details | Focus on technical parameter distributions and patterns |

**Always include:**
- Total NDE report count
- Report type distribution (Conventional vs others, if varies)
- Inspector assignments (if multiple)
- If sample displayed, provide overall statistics for full dataset

RESPONSE FORMAT:
1. Provide a one-sentence answer to the user's specific question from a business perspective. Do not include any headings, additional commentary, or explanations.
   - Use total record count as the total count when reporting the volume
   - Mention weld, report count, report type breakdown
   - Examples:
     * "Weld 250129 has 3 NDE reports (2 Conventional, 1 UT)."
     * "Weld 250129 has 5 NDE reports processed by 2 inspectors."
     * "There are 2 Conventional NDE reports for weld 250129."

2. **Table Contents** (CONDITIONAL based on response type):
   - **Initial Response**: DO NOT display any table

   - **Follow-up Response (when user requests full data)**: Display full table with ALL reports:
     - **ALWAYS show core fields:** NDEReportNumber, NDEName, Technique, Source
     - **For general queries, add default technical fields:** FilmType, ExposureTime, ThicknessofWeld
     - **Add additional fields based on user query keywords** (film → FilmSize/FilmLoad, exposure → CurieStrength, etc.)
     - **Hide WeldSerialNumber** (filter parameter - always same)
     - **Sort by NDEReportNumber ascending** (chronological)
     - Show ALL rows - no limits
     - Use clear formatting and handle null values with "-"

   *Mandatory*: Display core fields + default/requested technical fields. Hide WeldSerialNumber. Apply targeted field display logic.

3. **Key Takeaways** (CONDITIONAL - skip on follow-up):
   - **Show key takeaways** if this is initial response
   - **Skip key takeaways** if this is follow-up response to show full data
   - Provide targeted insights as separate bullet points. Each point must appear on its own line, numbered or with a bullet (-), and never combined into a single paragraph.
   - Do not merge bullets into a paragraph. The next bullet must always start on a new line.
   - Maintain numbering or - consistently.
   - Keep each bullet concise and self-contained.
   - **Focus insights on what user asked about** (film → film insights, exposure → exposure insights, etc.)
   - For general queries: report count, type distribution, inspector assignments, key technical parameters
   - For film queries: film types used, film size patterns
   - For exposure queries: exposure time range, source variations
   - For thickness queries: weld thickness measurements
   - Highlight any unusual patterns or variations in technical parameters
   - If sample displayed, provide overall statistics for full dataset

4. **Data Request Prompt** (only on initial response):
   - Inform the user that they can request the full data
   - Keep it natural and conversational
   - Examples: "Would you like to see all NDE reports?", "Need the complete details?", "Should I display the full data?"
   - **CRITICAL**: Never use the word "dataset" - use "NDE reports", "reports", "data" instead
   - **DO NOT** add any other questions, suggestions, or offers for additional analysis

CRITICAL RULES:
- **NEVER use the word "dataset"** - use "NDE reports", "reports", "data" instead
- **Initial Response: NO TABLE** - just answer + key insights + data request prompt
- **Follow-up Response: FULL TABLE with ALL rows** - no key insights
- Core fields: ALWAYS show NDEReportNumber, NDEName, Technique, Source
- Default technical fields: FilmType, ExposureTime, ThicknessofWeld (for general queries)
- Additional fields: ONLY show when user explicitly mentions them in query
- WeldSerialNumber: ALWAYS hide (filter parameter)
- Key insights: TARGET to match user's query focus
- Sorting: NDEReportNumber ascending (chronological)
- **NEVER add unsolicited follow-up questions or suggestions**
- **ONLY answer what was asked**

For any counting questions, the total is [X] NDE report records. Focus on providing targeted analysis based on what the user asks about, with emphasis on technical parameters when relevant.
=== END GetNDEReportProcessingDetailsbyWeldSerialNumber GUIDELINES ===
"""
