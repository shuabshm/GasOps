import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetWorkOrderNDEIndicationsbyCriteria(clean_data_array, api_parameters):
    """
    Performs data analysis for the GetWorkOrderNDEIndicationsbyCriteria API.
    
    This function processes grouped indication data. It calculates the overall 
    TOTAL count of indications (by summing the 'Count' field in the response)
    and the distribution of indication types.
    """
    total_grouped_records = len(clean_data_array)
    
    analysis_results = {
        "total_grouped_records": total_grouped_records, # Number of rows in the aggregated table
        "raw_data": clean_data_array,
        "filter_applied": api_parameters,
        "counts": {
            "total_indication_occurrences": 0, # <-- CRITICAL: Sum of the 'Count' field
            "indication_type_distribution": defaultdict(int),
            "grouping_field_distribution": defaultdict(int), # Distribution based on the non-Indication GroupBy field
        }
    }

    if total_grouped_records == 0:
        return analysis_results

    # --- Perform Statistical Analysis ---
    
    total_indication_occurrences = 0
    indication_type_counts = analysis_results["counts"]["indication_type_distribution"]
    grouping_field_counts = analysis_results["counts"]["grouping_field_distribution"]

    # Determine the primary grouping field (it's often the second element in the GroupBy array)
    group_by_fields = api_parameters.get('GroupBy', [])
    # Find the field that is NOT 'Indication' (e.g., WeldSerialNumber, WelderName)
    primary_grouping_field = next((field for field in group_by_fields if field != 'Indication'), None)
    
    for record in clean_data_array:
        try:
            # 1. Sum the 'Count' field to get the total number of defects
            count = int(record.get("Count", 0))
            total_indication_occurrences += count
            
            # 2. Count the distribution of specific NDE Indication types (e.g., Porosity, Crack)
            indication_type = record.get("Indication", "N/A")
            indication_type_counts[indication_type] += count # Tally by the total count, not by row
            
            # 3. Count the distribution based on the grouping field (e.g., Welder, Weld Serial Number)
            if primary_grouping_field:
                group_value = record.get(primary_grouping_field, "N/A")
                grouping_field_counts[group_value] += count # Tally by the total count
                
        except ValueError:
            logger.warning(f"Non-integer value found for 'Count' field in record.")

    analysis_results["counts"]["total_indication_occurrences"] = total_indication_occurrences
    
    # Format the distributions (based on total indication occurrences)
    def get_distributions(counts):
        if total_indication_occurrences == 0: return {}
        return {
            item: {
                "count": count, 
                "percentage": round((count / total_indication_occurrences) * 100, 2)
            }
            for item, count in counts.items()
        }

    analysis_results["counts"]["indication_type_distribution"] = get_distributions(indication_type_counts)
    
    # Only include grouping field distribution if a primary field was identified
    if primary_grouping_field:
        analysis_results["counts"]["grouping_field_distribution"] = get_distributions(grouping_field_counts)
    else:
        analysis_results["counts"]["grouping_field_distribution"] = {} # Clear if not relevant

    return analysis_results
