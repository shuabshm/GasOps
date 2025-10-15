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
            "unlocked_by_distribution": defaultdict(int),
            "weld_category_distribution": defaultdict(int), # <-- NEW DISTRIBUTION ADDED
            "pending_count": 0, # Welds pending edit (UpdatedDate is null/blank)
            "completed_count": 0
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis ---
    
    status_counts = analysis_results["counts"]["status_distribution"]
    unlocked_by_counts = analysis_results["counts"]["unlocked_by_distribution"]
    weld_category_counts = analysis_results["counts"]["weld_category_distribution"] # <-- NEW COUNT
    
    for record in clean_data_array:
        updated_date = record.get("UpdatedDate")
        unlocked_by = record.get("UnlockedBy", "Unknown")
        weld_category = record.get("WeldCategory", "Unknown") # <-- GET CATEGORY
        
        unlocked_by_counts[unlocked_by] += 1
        weld_category_counts[weld_category] += 1 # <-- COUNT CATEGORY
        
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
    analysis_results["counts"]["unlocked_by_distribution"] = get_distributions(unlocked_by_counts)
    analysis_results["counts"]["weld_category_distribution"] = get_distributions(weld_category_counts) # <-- ADD TO RESULTS
    
    return analysis_results
