import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetReshootDetailsbyWorkOrderNumberandCriteria(clean_data_array, api_parameters):
    """
    Performs data analysis for the GetReshootDetailsbyWorkOrderNumberandCriteria API.
    
    This function counts total records and analyzes the distribution of reshoot status 
    (RequiredReshoot) and completion status (UpdateCompleted).
    """
    total_records = len(clean_data_array)
    
    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,  # Full list of reshoot records
        "filter_applied": api_parameters,
        "counts": {
            "required_reshoot_distribution": {},
            "update_completed_distribution": {},
            "nde_report_number_distribution": {},
            "weld_serial_numbers_distribution": {},
            "action_required_count": 0 # Welds that are 'Required: Yes' and 'Completed: No'
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis ---

    required_reshoot_counts = defaultdict(int)
    update_completed_counts = defaultdict(int)
    nde_report_number_counts = defaultdict(int)
    weld_serial_numbers_counts = defaultdict(int)
    action_required_count = 0

    for record in clean_data_array:
        required = record.get("RequiredReshoot", "Unknown")
        completed = record.get("UpdateCompleted", "Unknown")

        required_reshoot_counts[required] += 1
        update_completed_counts[completed] += 1
        nde_report_number_counts[record.get("NDEReportNumber", "Unknown")] += 1
        weld_serial_numbers_counts[record.get("WeldSerialNumbers", "Unknown")] += 1

        # Critical workflow metric: Welds needing action
        if required == "Yes" and completed == "No":
            action_required_count += 1

    # Format the distributions with counts and percentages
    def get_distributions(counts):
        if total_records == 0: return {}
        return {
            item: {"count": count, "percentage": (count / total_records) * 100}
            for item, count in counts.items()
        }

    analysis_results["counts"]["required_reshoot_distribution"] = get_distributions(required_reshoot_counts)
    analysis_results["counts"]["update_completed_distribution"] = get_distributions(update_completed_counts)
    analysis_results["counts"]["nde_report_number_distribution"] = get_distributions(nde_report_number_counts)
    analysis_results["counts"]["weld_serial_numbers_distribution"] = get_distributions(weld_serial_numbers_counts)
    analysis_results["counts"]["action_required_count"] = action_required_count

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_nde_report_numbers": len(set(record.get("NDEReportNumber") for record in clean_data_array if record.get("NDEReportNumber") and record.get("NDEReportNumber").strip())),
        "total_distinct_weld_serial_numbers": len(set(record.get("WeldSerialNumbers") for record in clean_data_array if record.get("WeldSerialNumbers"))),
        "total_distinct_required_reshoot": len(set(record.get("RequiredReshoot") for record in clean_data_array if record.get("RequiredReshoot"))),
        "total_distinct_update_completed": len(set(record.get("UpdateCompleted") for record in clean_data_array if record.get("UpdateCompleted")))
    }

    return analysis_results
