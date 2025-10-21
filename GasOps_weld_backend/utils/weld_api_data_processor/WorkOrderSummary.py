def analyze_WorkOrderSummary(api_results, api_parameters):
    """
    Processes and consolidates data from multiple APIs into a single,
    structured dictionary for the LLM to analyze and format.
    """
    work_order_info = {}
    weld_details_data = []

    for result in api_results:
        if result["api_name"] == "GetWorkOrderInformation":
            if result["data"] and result["data"].get("Data"):
                work_order_info = result["data"]["Data"][0]
        elif result["api_name"] == "GetWeldDetailsbyWorkOrderNumberandCriteria":
            if result["data"] and result["data"].get("Data"):
                weld_details_data = result["data"]["Data"]

    # Pre-processing: Extract counts and distributions
    status_counts = {}
    welder_counts = {}

    for weld in weld_details_data:
        # Tally CWI status distributions
        cwi_result = weld.get("CWIResult")
        if cwi_result:
            status_counts[cwi_result] = status_counts.get(cwi_result, 0) + 1

        # Tally welds per welder (assuming Welder1 through Welder4)
        for i in range(1, 5):
            welder_field = weld.get(f"Welder{i}")
            if welder_field:
                welder_name = welder_field.split('(')[0].strip()
                welder_counts[welder_name] = welder_counts.get(welder_name, 0) + 1

    # Format the data for the LLM
    return {
        "api_name": "WorkOrderSummaryDashboard",
        "filter_applied": api_parameters,
        "preprocessed_data": {
            "work_order_details": {
                "WorkOrderNumber": work_order_info.get("WorkOrderNumber"),
                "WorkOrderStatusDescription": work_order_info.get("WorkOrderStatusDescription"),
                "ProjectNumber": work_order_info.get("ProjectNumber"),
                "Region": work_order_info.get("Region"),
                "Location": work_order_info.get("Location")
            },
            "weld_metrics": {
                "total_welds": len(weld_details_data),
                "cwi_status_breakdown": status_counts,
                "welder_assignments": sorted(welder_counts.items(), key=lambda item: item[1], reverse=True)
            }
        }
    }