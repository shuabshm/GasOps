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
            "work_order_number_distribution": defaultdict(int),
            "project_number_distribution": defaultdict(int)
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis ---

    work_order_number_counts = analysis_results["counts"]["work_order_number_distribution"]
    project_number_counts = analysis_results["counts"]["project_number_distribution"]

    for record in clean_data_array:
        work_order_number_counts[record.get("WorkOrderNumber", "Unknown")] += 1
        project_number_counts[record.get("ProjectNumber", "Unknown")] += 1
        
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

    analysis_results["counts"]["work_order_number_distribution"] = get_distributions(work_order_number_counts)
    analysis_results["counts"]["project_number_distribution"] = get_distributions(project_number_counts)

    # Add distinct counts (excluding Location as per user request)
    analysis_results["distinct_counts"] = {
        "total_distinct_work_order_numbers": len(set(record.get("WorkOrderNumber") for record in clean_data_array if record.get("WorkOrderNumber"))),
        "total_distinct_project_numbers": len(set(record.get("ProjectNumber") for record in clean_data_array if record.get("ProjectNumber")))
    }

    return analysis_results
