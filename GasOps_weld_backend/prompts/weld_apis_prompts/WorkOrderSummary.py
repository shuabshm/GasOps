import json
def get_api_prompt(analysis_results):
    preprocessed_data = analysis_results.get("preprocessed_data", {})
    work_order_info = preprocessed_data.get("work_order_details", {})
    weld_metrics = preprocessed_data.get("weld_metrics", {})

    # Build the welder list for the prompt
    welder_list = "\n".join([f"- {name}: {count} welds" for name, count in weld_metrics.get("welder_assignments", [])])
    if not welder_list:
        welder_list = "- No welders found."

    # Build the status breakdown table as a string
    status_breakdown = "| Status | Count |\n|---|---|\n"
    for status, count in weld_metrics.get("cwi_status_breakdown", {}).items():
        status_breakdown += f"| {status} | {count} |\n"
    if not weld_metrics.get("cwi_status_breakdown"):
        status_breakdown = "No CWI status data available."

    return f"""
You are an expert data analyst for WeldInsights. Your task is to provide a comprehensive summary for a work order. You have been provided with preprocessed data from multiple APIs, consolidated into a single JSON object.

Data to analyze:
{json.dumps(analysis_results, indent=2)}

Instructions:
1.  **High-Level Summary**: Start with a single, clear, and concise sentence that provides an overview of the work order, including its status, number of welds, and project number.
2.  **Work Order Details Table**: Create a markdown table with two columns, "Field" and "Value". Populate this table with the work order details provided in the `work_order_details` section of the data.
3.  **Weld Status Table**: Create a markdown table titled 'Weld Status Breakdown'. This table should have two columns: 'Status' and 'Count'. Populate this table using the `cwi_status_breakdown` data.
4.  **Welder Assignments List**: Create a bulleted list titled 'Welder Assignments'. For each welder, list the number of welds they worked on. Sort this list from most to least active.
5.  **Do not add any other information, commentary, or conversational phrases.** Just provide the summary sentence, followed by the tables and list in the specified format.
6.  If any data is unavailable, display 'N/A' or '0'.
"""