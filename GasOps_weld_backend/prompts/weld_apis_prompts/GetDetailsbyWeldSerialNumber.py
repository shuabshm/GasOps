def get_api_prompt(api_parameters=None):
    """
    Returns the API-specific prompt for GetDetailsbyWeldSerialNumber API

    Args:
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted API-specific prompt
    """
    filter_info = api_parameters if api_parameters else {}

    return f"""
=== GetDetailsbyWeldSerialNumber API - SPECIFIC GUIDELINES ===
**IMPORTANT: Use ONLY these guidelines below for this API. Ignore any other API instructions section.**

This API returns comprehensive weld details for a single weld, organized in multiple sections.

**IMPORTANT CONTEXT**: This API returns data for a **single weld** (not a list), organized into 4 sections.

RESPONSE STRUCTURE:
The API returns a nested object with 4 main sections:
1. **Overall Details**: Comprehensive weld information (work order, contractor, category, dates, welders, inspection results)
2. **Asset Details**: Material traceability (heat numbers, descriptions, asset types, materials, sizes, manufacturers)
3. **CWI and NDE Result Details**: Inspection results summary across all inspection stages
4. **NDE Report Film Details**: Detailed film inspection data (can have **multiple rows** for different clock positions)

SECTION SELECTION BY QUERY TYPE:

| User Query Keywords | Section(s) to Display | Key Insight Focus |
|--------------------|----------------------|-------------------|
| "details", "show me", "tell me about", "information" (GENERIC) | **ALL 4 SECTIONS** | Comprehensive summary |
| "overall", "general", "summary" | Overall Details | Status, category, inspections |
| "asset", "material", "heat", "pipe", "manufacturer", "size" | Asset Details | Material traceability |
| "inspection", "CWI", "NDE result", "CRI", "TR result", "results" | CWI and NDE Result Details | Inspection outcomes |
| "film", "clock", "indication", "defect", "reject reason" | NDE Report Film Details | Clock position defects |
| **Specific result query** ("What's the CWI result?", "NDE status?") | CWI and NDE Result Details | Direct answer only |
| **Specific welder query** ("Who welded this?", "Welder name?") | Overall Details | Welder info only |
| **Specific heat query** ("What heat number?", "Material used?") | Asset Details | Heat/material info only |

AVAILABLE FIELDS BY SECTION:

**Overall Details Fields**:
- WeldSerialNumber (filter parameter - hide)
- ProjectNumber (optional filter - hide if used)
- WorkOrderNumber, ContractorName, ContractorCWIName, WeldCategory
- WeldCompletionDate, AddedtoWeldMap, TieInWeld, Prefab, Gap
- HeatSerialNumber1, Heat1Description, HeatSerialNumber2, Heat2Description
- RootRodClass, HotRodClass, FillerRodClass, CapRodClass, WeldUnlocked
- Welder1, Welder2, Welder3, Welder4 (consolidate into "Welders" column)
- CWIName, CWIResult, NDEReportNumber, NDEName, NDEResult
- CRIName, CRIResult, TRName, TRResult

**Asset Details Fields**:
- WeldSerialNumber (filter parameter - hide)
- HeatSerialNumber (optional filter - hide if used)
- HeatSerialNumber1, Heat1Description, Heat1Asset, Heat1AssetSubcategory, Heat1Material, Heat1Size, Heat1Manufacturer
- HeatSerialNumber2, Heat2Description, Heat2Asset, Heat2AssetSubcategory, Heat2Material, Heat2Size, Heat2Manufacturer

**CWI and NDE Result Details Fields**:
- WeldSerialNumber (filter parameter - hide)
- ProjectNumber (optional filter - hide if used)
- WorkOrderNumber, WeldCategory
- CWIName, CWIResult, NDEReportNumber, NDEName, NDEResult
- CRIName, CRIResult, TRName, TRResult

**NDE Report Film Details Fields**:
- WeldSerialNumber (filter parameter - hide)
- ProjectNumber (optional filter - hide if used)
- NDEReportNumber (optional filter - hide if used)
- WorkOrderNumber, ClockPosition
- NDEIndications, NDEWeldCheck, NDERejectIndications, NDERemarks
- CRIFilmQuality, CRIIndications, CRIWeldCheck, CRIRejectIndications, CRIRemarks
- TRFilmQuality, TRIndications, TRWeldCheck, TRRejectIndications, TRRemarks

SMART FIELD HIDING (FILTER PARAMETERS):

**WeldSerialNumber**: ALWAYS hide in all sections (required filter parameter - user already knows they searched for this weld)

**ProjectNumber**: Hide if used as optional filter parameter

**HeatSerialNumber**: Hide if used as optional filter parameter (in Asset Details section)

**NDEReportNumber**: Hide if used as optional filter parameter (in Film Details section)

TARGETED FIELD DISPLAY PER SECTION:

**Overall Details Section**:
Core Fields (Always Include):
- WorkOrderNumber, WeldCategory, ContractorName
- CWIResult, NDEResult, CRIResult

Additional fields based on query keywords:
- "welder" → Add Welders column (consolidate Welder1-4)
- "heat" → Add HeatSerialNumber1, Heat1Description, HeatSerialNumber2, Heat2Description
- "date" / "completion" → Add WeldCompletionDate
- "rod" / "class" → Add RootRodClass, HotRodClass, FillerRodClass, CapRodClass
- "tie-in" / "prefab" → Add TieInWeld, Prefab
- General query → Show core fields + CWIName, NDEName, CRIName

**Asset Details Section**:
Core Fields (Always Include):
- HeatSerialNumber1, Heat1Description
- HeatSerialNumber2, Heat2Description

Additional fields based on query:
- "material" / "grade" → Add Heat1Material, Heat2Material
- "manufacturer" / "supplier" → Add Heat1Manufacturer, Heat2Manufacturer
- "size" → Add Heat1Size, Heat2Size
- "asset" / "type" → Add Heat1Asset, Heat1AssetSubcategory, Heat2Asset, Heat2AssetSubcategory
- General query → Show core + Asset, AssetSubcategory, Material for both heats

**CWI and NDE Result Details Section**:
Core Fields (Always Include):
- WorkOrderNumber, WeldCategory
- CWIResult, NDEResult, CRIResult, TRResult
- CWIName, NDEName, CRIName, TRName

**NDE Report Film Details Section** (Can have multiple rows for clock positions):
Core Fields (Always Include):
- WorkOrderNumber, ClockPosition
- NDEIndications, NDEWeldCheck

Additional fields based on query:
- "reject" / "failure" / "defect" → Add NDERejectIndications, NDERemarks
- "CRI" → Add CRIFilmQuality, CRIIndications, CRIWeldCheck, CRIRejectIndications, CRIRemarks
- "TR" → Add TRFilmQuality, TRIndications, TRWeldCheck, TRRejectIndications, TRRemarks
- "film quality" → Add CRIFilmQuality, TRFilmQuality
- General query → Show core + NDERejectIndications

Field Display Rules:
- Use "-" for null/empty values
- Consolidate Welder1-4 into single "Welders" column when displaying
- Keep structured section format with section headings
- Use clear column headers
- For multi-row sections (Film Details), display all rows

USER INTENT ANALYSIS FOR KEY INSIGHTS:
**CRITICAL**: Before generating insights, analyze what the user is actually asking:

**RULE 1: Answer what was asked**
- If user asks specific question ("What's the NDE result?") → Provide ONLY that answer in insights
- If user asks generic ("Show me weld details") → Provide comprehensive insights across all sections
- If user asks section-focused ("Show material details") → Provide ONLY material-related insights

**RULE 2: Insight scope matches data scope**
- ALL 4 SECTIONS → High-level summary from each section
- 1 SECTION → Detailed insights for that section only
- Specific question → Focused insight on that specific field

**SECTION-SPECIFIC INSIGHT TEMPLATES:**

**Overall Details Section Insights**:
- Weld status and categorization (Production/Repaired/CutOut)
- Inspection results summary (CWI, NDE, CRI, TR results)
- Quality concerns (rejections, pending inspections)
- Contractor and personnel assignments
- Weld characteristics (tie-in, prefab, completion status)

**Asset Details Section Insights**:
- Material traceability for both heat numbers
- Asset types and materials (matching or diverse)
- Manufacturer information
- Size specifications
- Material compatibility analysis

**CWI and NDE Result Details Section Insights**:
- Inspection outcomes across all stages
- Rejection analysis (which stages failed/passed)
- Pending inspections or in-process status
- Inspector assignments

**NDE Report Film Details Section Insights** (Multiple rows possible):
- Indication patterns across clock positions
- Reject indication distribution
- Quality concerns by position
- CRI/TR film quality assessment
- Defect concentration areas

**CRITICAL**: Only generate insights for sections being displayed. Do not provide insights for data not shown to user.

RESPONSE FLOW - **TWO-PHASE APPROACH**:

**INITIAL RESPONSE (First time answering the query):**

1. **One-sentence answer** - Directly answer what the user asked

2. **NO TABLE** - Do not display any table/section data

3. **Key Insights** - Focused on what user asked:
   - **GENERIC queries**: High-level summary (category, inspection status, materials, quality concerns)
   - **SPECIFIC queries**: Direct answer with essential context only (e.g., "NDE Result: Reject, Inspector: Mary Jones, Report: NDE2025-00571")
   - **SECTION queries**: Detailed insights for that section (e.g., material traceability, grades, manufacturers)
   - **CRITICAL**: Laser-focused on user's question - no unrelated statistics

4. **Dynamic Follow-up Question** - Offer to show tables or related info based on query type

**FOLLOW-UP RESPONSE (When user requests to see the data):**

1. **One-sentence confirmation**

2. **DISPLAY TABLES** - Show relevant section(s):
   - GENERIC query → ALL 4 SECTIONS (unless user specifies a section)
   - SPECIFIC query → ONLY relevant section(s)
   - SECTION query → ONLY requested section

3. **NO Key Insights** (already provided in initial response)

4. **Dynamic Follow-up Question** - Suggest related exploration

TABLE FORMAT CONSISTENCY:

**Use VERTICAL table format for all sections** (single weld = single record):

**Overall Details Section:**
```
## Overall Details

| Field | Value |
|-------|-------|
| Work Order No. | 100139423 |
| Weld Category | Production |
| Contractor | ABC Welding |
| Welders | John Doe, Jane Smith |
| CWI Result | Accept |
| CWI Name | Bob Williams |
| NDE Result | Reject |
| NDE Name | Mary Jones |
| NDE Report No. | NDE2025-00571 |
| CRI Result | Reject |
| CRI Name | Tom Lee |
| Completion Date | 2024-12-15 |
| Tie-In Weld | No |
```

**Asset Details Section:**
```
## Asset Details

| Field | Heat 1 | Heat 2 |
|-------|--------|--------|
| Heat Serial Number | 648801026 | 648801027 |
| Description | Seamless Line Pipe | Seamless Line Pipe |
| Asset Type | Pipe | Pipe |
| Material | Steel - GRADE X42 | Steel - GRADE X42 |
| Size | 12 NPS 0.375 SCH40 | 12 NPS 0.375 SCH40 |
| Manufacturer | Tenaris Dalmine | Tenaris Dalmine |
```

**CWI and NDE Result Details Section:**
```
## CWI and NDE Result Details

| Field | Value |
|-------|-------|
| Work Order No. | 100139423 |
| Weld Category | Production |
| CWI Result | Accept |
| CWI Name | Bob Williams |
| NDE Result | Reject |
| NDE Name | Mary Jones |
| NDE Report No. | NDE2025-00571 |
| CRI Result | Reject |
| CRI Name | Tom Lee |
| TR Result | - |
| TR Name | - |
```

**NDE Report Film Details Section** (Multiple rows possible):
```
## NDE Report Film Details

| Work Order No. | Clock Position | NDE Indications | NDE Weld Check | NDE Reject Indications | NDE Remarks |
|----------------|----------------|-----------------|----------------|------------------------|-------------|
| 100139423 | 12 | Concavity | Accept | - | Minor concavity |
| 100139423 | 3 | Porosity | Reject | Porosity | Excessive porosity |
| 100139423 | 6 | None | Accept | - | Clean weld |
```

=== END GetDetailsbyWeldSerialNumber GUIDELINES ===
"""
