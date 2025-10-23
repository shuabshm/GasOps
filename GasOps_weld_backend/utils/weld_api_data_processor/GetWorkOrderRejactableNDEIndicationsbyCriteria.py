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
            "total_rejectable_occurrences": 0,
            "rejectable_indication_type_distribution": defaultdict(int),
        }
    }

    if total_grouped_records == 0:
        return analysis_results

    # --- Setup Aggregators ---
    total_rejectable_occurrences = 0
    indication_type_counts = analysis_results["counts"]["rejectable_indication_type_distribution"]
    
    # --- Core Aggregation Loop ---
    for record in clean_data_array:
        try:
            # 1. Sum the 'Count' field to get the total number of critical defects (Crucial Metric)
            count = int(record.get("Count", 0))
            total_rejectable_occurrences += count
            
            # 2. Indication Type Distribution: Tally by the defect count
            indication_type = record.get("Indication", "N/A")
            indication_type_counts[indication_type] += count 
                
        except ValueError:
            logger.warning(f"Non-integer value found for 'Count' field in record.")

    analysis_results["counts"]["total_rejectable_occurrences"] = total_rejectable_occurrences
    
    # --- Format Distributions ---
    
    # Helper to calculate distributions with 2 decimal places based on total rejectable occurrences
    def get_distributions(counts):
        if total_rejectable_occurrences == 0: return {}
        return {
            item: {
                "count": count, 
                "percentage": round((count / total_rejectable_occurrences) * 100, 2)
            }
            for item, count in counts.items()
        }

    # Final Distribution: ONLY the Indication Type Distribution
    analysis_results["counts"]["rejectable_indication_type_distribution"] = get_distributions(indication_type_counts)
    
    # Remove the placeholder for the grouping distribution entirely
    # The AI will perform the workload breakdown (Welder distribution) directly from the 'raw_data' table rows.
    
    return analysis_results
