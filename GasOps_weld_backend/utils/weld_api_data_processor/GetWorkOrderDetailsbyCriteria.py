import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetWorkOrderDetailsbyCriteria(clean_data_array, api_parameters):
    """
    Performs data analysis for the GetWorkOrderDetailsbyCriteria API.
    
    This API is a lookup function. This transformer calculates total records and 
    distributions for ProjectNumber and Location.
    """
    total_records = len(clean_data_array)
    
    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,  # Full list of work order records
        "filter_applied": api_parameters,
        "counts": {
            "project_distribution": defaultdict(int),
            "location_distribution": defaultdict(int),
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis ---
    
    project_counts = analysis_results["counts"]["project_distribution"]
    location_counts = analysis_results["counts"]["location_distribution"]
    
    for record in clean_data_array:
        project_counts[record.get("ProjectNumber", "N/A")] += 1
        location_counts[record.get("Location", "N/A")] += 1
        
    # Format the distributions with counts and percentages (rounded to 2 decimal places)
    def get_distributions(counts):
        if total_records == 0: return {}
        return {
            item: {
                "count": count, 
                "percentage": round((count / total_records) * 100, 2)
            }
            for item, count in counts.items()
        }

    analysis_results["counts"]["project_distribution"] = get_distributions(project_counts)
    analysis_results["counts"]["location_distribution"] = get_distributions(location_counts)
    
    return analysis_results
