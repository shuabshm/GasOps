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
            "action_required_count": 0 # Welds that are 'Required: Yes' and 'Completed: No'
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis ---
    
    required_reshoot_counts = defaultdict(int)
    update_completed_counts = defaultdict(int)
    action_required_count = 0
    
    for record in clean_data_array:
        required = record.get("RequiredReshoot", "Unknown")
        completed = record.get("UpdateCompleted", "Unknown")
        
        required_reshoot_counts[required] += 1
        update_completed_counts[completed] += 1
        
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
    analysis_results["counts"]["action_required_count"] = action_required_count
    
    return analysis_results
