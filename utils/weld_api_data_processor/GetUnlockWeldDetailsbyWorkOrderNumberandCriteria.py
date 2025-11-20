import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetUnlockWeldDetailsbyWorkOrderNumberandCriteria(clean_data_array, api_parameters):
    """
    Performs data analysis for the GetUnlockWeldDetailsbyWorkOrderNumberandCriteria API.
    
    This function counts total records and analyzes the distribution of workflow status
    (Pending/Completed), accountability (UnlockedBy), and the type of weld (WeldCategory).
    """
    total_records = len(clean_data_array)
    
    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,  # Full list of unlocked weld records
        "filter_applied": api_parameters,
        "counts": {
            "status_distribution": defaultdict(int),
            "weld_serial_number_distribution": defaultdict(int),
            "project_number_distribution": defaultdict(int),
            "weld_category_distribution": defaultdict(int),
            "contractor_name_distribution": defaultdict(int),
            "welder_distribution": defaultdict(int),
            "contractor_cwi_name_distribution": defaultdict(int),
            "cwi_name_distribution": defaultdict(int),
            "unlocked_by_distribution": defaultdict(int),
            "unlocked_date_distribution": defaultdict(int),
            "update_completed_distribution": defaultdict(int),
            "updated_by_distribution": defaultdict(int),
            "updated_date_distribution": defaultdict(int),
            "pending_count": 0, # Welds pending edit (UpdatedDate is null/blank)
            "completed_count": 0
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis ---

    status_counts = analysis_results["counts"]["status_distribution"]
    weld_serial_number_counts = analysis_results["counts"]["weld_serial_number_distribution"]
    project_number_counts = analysis_results["counts"]["project_number_distribution"]
    weld_category_counts = analysis_results["counts"]["weld_category_distribution"]
    contractor_name_counts = analysis_results["counts"]["contractor_name_distribution"]
    welder_counts = analysis_results["counts"]["welder_distribution"]
    contractor_cwi_name_counts = analysis_results["counts"]["contractor_cwi_name_distribution"]
    cwi_name_counts = analysis_results["counts"]["cwi_name_distribution"]
    unlocked_by_counts = analysis_results["counts"]["unlocked_by_distribution"]
    unlocked_date_counts = analysis_results["counts"]["unlocked_date_distribution"]
    update_completed_counts = analysis_results["counts"]["update_completed_distribution"]
    updated_by_counts = analysis_results["counts"]["updated_by_distribution"]
    updated_date_counts = analysis_results["counts"]["updated_date_distribution"]

    for record in clean_data_array:
        updated_date = record.get("UpdatedDate")

        # Count all distributions
        weld_serial_number_counts[record.get("WeldSerialNumber", "Unknown")] += 1
        project_number_counts[record.get("ProjectNumber", "Unknown")] += 1
        weld_category_counts[record.get("WeldCategory", "Unknown")] += 1
        contractor_name_counts[record.get("ContractorName", "Unknown")] += 1
        contractor_cwi_name_counts[record.get("ContractorCWIName", "Unknown")] += 1
        cwi_name_counts[record.get("CWIName", "Unknown")] += 1
        unlocked_by_counts[record.get("UnlockedBy", "Unknown")] += 1
        unlocked_date_counts[record.get("UnlockedDate", "Unknown")] += 1
        update_completed_counts[record.get("UpdateCompleted", "Unknown")] += 1
        updated_by_counts[record.get("UpdatedBy", "Unknown")] += 1
        updated_date_counts[record.get("UpdatedDate", "Unknown")] += 1

        # Consolidate all welders (Welder1, Welder2, Welder3, Welder4)
        for welder_field in ["Welder1", "Welder2", "Welder3", "Welder4"]:
            welder = record.get(welder_field, "").strip()
            if welder:  # Only count non-empty welder fields
                welder_counts[welder] += 1

        # Determine Status: Pending is critical business logic (UpdatedDate is null/blank)
        if not updated_date or str(updated_date).strip() == "":
            status_counts['Pending'] += 1
        else:
            status_counts['Completed'] += 1

    # Finalize the counts dictionary
    analysis_results["counts"]["pending_count"] = status_counts['Pending']
    analysis_results["counts"]["completed_count"] = status_counts['Completed']
    
    # Format the distributions with counts and percentages
    def get_distributions(counts):
        if total_records == 0: return {}
        return {
            item: {"count": count, "percentage": (count / total_records) * 100}
            for item, count in counts.items()
        }

    analysis_results["counts"]["status_distribution"] = get_distributions(status_counts)
    analysis_results["counts"]["weld_serial_number_distribution"] = get_distributions(weld_serial_number_counts)
    analysis_results["counts"]["project_number_distribution"] = get_distributions(project_number_counts)
    analysis_results["counts"]["weld_category_distribution"] = get_distributions(weld_category_counts)
    analysis_results["counts"]["contractor_name_distribution"] = get_distributions(contractor_name_counts)
    analysis_results["counts"]["welder_distribution"] = get_distributions(welder_counts)
    analysis_results["counts"]["contractor_cwi_name_distribution"] = get_distributions(contractor_cwi_name_counts)
    analysis_results["counts"]["cwi_name_distribution"] = get_distributions(cwi_name_counts)
    analysis_results["counts"]["unlocked_by_distribution"] = get_distributions(unlocked_by_counts)
    analysis_results["counts"]["unlocked_date_distribution"] = get_distributions(unlocked_date_counts)
    analysis_results["counts"]["update_completed_distribution"] = get_distributions(update_completed_counts)
    analysis_results["counts"]["updated_by_distribution"] = get_distributions(updated_by_counts)
    analysis_results["counts"]["updated_date_distribution"] = get_distributions(updated_date_counts)

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_weld_serial_numbers": len(set(record.get("WeldSerialNumber") for record in clean_data_array if record.get("WeldSerialNumber"))),
        "total_distinct_project_numbers": len(set(record.get("ProjectNumber") for record in clean_data_array if record.get("ProjectNumber"))),
        "total_distinct_weld_categories": len(set(record.get("WeldCategory") for record in clean_data_array if record.get("WeldCategory"))),
        "total_distinct_contractor_names": len(set(record.get("ContractorName") for record in clean_data_array if record.get("ContractorName") and record.get("ContractorName").strip())),
        "total_distinct_welders": len(set(record.get(f"Welder{i}") for record in clean_data_array for i in range(1, 5) if record.get(f"Welder{i}") and record.get(f"Welder{i}").strip())),
        "total_distinct_contractor_cwi_names": len(set(record.get("ContractorCWIName") for record in clean_data_array if record.get("ContractorCWIName") and record.get("ContractorCWIName").strip())),
        "total_distinct_cwi_names": len(set(record.get("CWIName") for record in clean_data_array if record.get("CWIName") and record.get("CWIName").strip())),
        "total_distinct_unlocked_by": len(set(record.get("UnlockedBy") for record in clean_data_array if record.get("UnlockedBy") and record.get("UnlockedBy").strip())),
        "total_distinct_unlocked_dates": len(set(record.get("UnlockedDate") for record in clean_data_array if record.get("UnlockedDate"))),
        "total_distinct_update_completed": len(set(record.get("UpdateCompleted") for record in clean_data_array if record.get("UpdateCompleted"))),
        "total_distinct_updated_by": len(set(record.get("UpdatedBy") for record in clean_data_array if record.get("UpdatedBy") and record.get("UpdatedBy").strip())),
        "total_distinct_updated_dates": len(set(record.get("UpdatedDate") for record in clean_data_array if record.get("UpdatedDate")))
    }

    return analysis_results
