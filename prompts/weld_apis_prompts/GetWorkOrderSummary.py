def get_api_prompt(work_order_number, processed_apis, api_parameters=None):
    """
    Returns the synthesis prompt for GetWorkOrderSummary API.

    This prompt is used to generate a comprehensive work order summary
    from pre-processed data from multiple APIs (using their transformers).

    Args:
        work_order_number (str): The work order number being summarized
        processed_apis (list): List of dicts containing pre-processed data from each API:
            - api_name: Name of the API
            - section_title: Human-readable section name
            - analysis_results: Pre-processed data from transformer (without raw_data)
            - total_records: Count of records
        api_parameters (dict): Optional dictionary of API filter parameters

    Returns:
        str: The formatted synthesis prompt
    """
    import json

    # Build sections from pre-processed data
    sections = []

    for api_data in processed_apis:
        api_name = api_data.get("api_name", "Unknown")
        section_title = api_data.get("section_title", api_name)
        analysis_results = api_data.get("analysis_results", {})
        total_records = api_data.get("total_records", 0)

        # Remove raw_data to keep prompt focused
        analysis_for_prompt = {k: v for k, v in analysis_results.items() if k != 'raw_data'}

        if total_records == 0:
            sections.append(f"""
### {section_title}
No data available for this section.
""")
        else:
            sections.append(f"""
### {section_title}
Total Records: {total_records}

Data:
{json.dumps(analysis_for_prompt, indent=2, default=str)}
""")

    combined_sections = "\n".join(sections)

    return f"""
=== GetWorkOrderSummary - Comprehensive Analysis Guidelines ===

You are generating a comprehensive work order summary from pre-processed data from multiple APIs.

Work Order Number: {work_order_number}

**Available Data:**
{combined_sections}

**Your Task:**
Create a cohesive, well-structured, narrative work order summary by analyzing and synthesizing the pre-processed data above.

**OUTPUT STRUCTURE:**

# Work Order [WorkOrderNumber] - Comprehensive Summary

## Overview
[Write 2-3 paragraphs providing a high-level overview of the work order, including:
- What is this work order (project, location, region, contractor)
- Overall scale (total welds, number of welders)
- Overall quality status (inspection completion, acceptance rates)
- Current status and any critical items]

## Work Order Details
[Synthesize from "Work Order Information" section:
- Project and location information
- Contractor and personnel assignments
- Work order type and status]

## Weld Production Summary
[Synthesize from "Weld Details & Inspection Results" and "Welder Performance" sections:
- Total welds and breakdown by category (Production/Repaired/CutOut)
- Key weld characteristics (tie-ins, prefabs, gaps, etc.)
- Welder contributions and top performers
- Position-wise breakdown if relevant]

## Inspection Results & Quality
[Synthesize from inspection-related sections:
- CWI/NDE/CRI inspection completion and results
- Acceptance and rejection statistics
- Inspector assignments and workload]

## Quality Issues & Indications
[Synthesize from NDE/CRI Indications sections:
- Types and frequencies of indications found
- Rejectable indications requiring attention
- Severity assessment (HIGH/MEDIUM/LOW priority)]

## Reshoots & Rework
[Synthesize from "Reshoot Details" section:
- Number of reshoots and reasons
- Completion status
- Action items if any]

## Key Insights & Observations
[Provide analytical insights by identifying patterns across all sections:
- Overall quality trends
- Performance highlights or concerns
- Risk areas or items needing attention
- Recommendations if applicable]

**FORMATTING GUIDELINES:**
1. **Use clear, descriptive narrative language** - Write in complete sentences and paragraphs
2. **Use absolute numbers only** - No percentages (e.g., "450 welds accepted" not "90%")
3. **Be comprehensive but concise** - Include all important information, avoid redundancy
4. **Use proper section headers** - Use ## for main sections
5. **Use bullet points sparingly** - Only for lists of similar items
6. **Highlight critical items** - Use ➡️ for items requiring attention
7. **Maintain professional tone** - Technical but accessible language
8. **NO follow-up questions** - This is a complete, standalone report

**SYNTHESIS STRATEGY:**
- Look for connections and patterns across different sections
- Identify correlations (e.g., which welders have high rejection rates)
- Provide context (e.g., "This is higher/lower than typical")
- Prioritize actionable information
- Consolidate duplicate information from multiple sections

Create a comprehensive summary that someone unfamiliar with the work order can understand the complete picture.
=== END GetWorkOrderSummary Synthesis Guidelines ===
"""
