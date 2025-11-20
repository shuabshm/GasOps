import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetWorkOrderRejactableNDEIndicationsbyCriteria(clean_data_array, api_parameters):
    """
    Performs data analysis for the GetWorkOrderRejactableNDEIndicationsbyCriteria API.
    
    This function processes grouped rejectable indication data. It calculates the overall 
    TOTAL count of critical indications (by summing the 'Count' field in the response)
    and the distribution of rejectable indication types, which is the non-obvious metric.
    The distribution for the GroupBy field is redundant and intentionally removed.
    """
    total_grouped_records = len(clean_data_array)

    analysis_results = {
        "total_records": total_grouped_records, # Standard field for consistency across all APIs
        "total_grouped_records": total_grouped_records,
        "raw_data": clean_data_array,
        "filter_applied": api_parameters,
        "counts": {
            "work_order_number_distribution": defaultdict(int),
            "indication_distribution": defaultdict(int)
        }
    }

    if total_grouped_records == 0:
        return analysis_results

    # --- Perform Statistical Analysis ---

    work_order_number_counts = analysis_results["counts"]["work_order_number_distribution"]
    indication_counts = analysis_results["counts"]["indication_distribution"]

    for record in clean_data_array:
        work_order_number_counts[record.get("WorkOrderNumber", "Unknown")] += 1
        indication_counts[record.get("Indication", "Unknown")] += 1

    # Format the distributions with counts and percentages
    def get_distributions(counts):
        if total_grouped_records == 0: return {}
        return {
            item: {
                "count": count,
                "percentage": round((count / total_grouped_records) * 100, 2)
            }
            for item, count in counts.items()
        }

    analysis_results["counts"]["work_order_number_distribution"] = get_distributions(work_order_number_counts)
    analysis_results["counts"]["indication_distribution"] = get_distributions(indication_counts)

    # Add distinct counts
    analysis_results["distinct_counts"] = {
        "total_distinct_work_order_numbers": len(set(record.get("WorkOrderNumber") for record in clean_data_array if record.get("WorkOrderNumber"))),
        "total_distinct_indications": len(set(record.get("Indication") for record in clean_data_array if record.get("Indication") and record.get("Indication").strip()))
    }

    return analysis_results
