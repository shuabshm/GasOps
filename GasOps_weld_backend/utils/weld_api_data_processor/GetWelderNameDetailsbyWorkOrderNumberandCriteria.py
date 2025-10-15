import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetWelderNameDetailsbyWorkOrderNumberandCriteria(clean_data_array, api_parameters):
    """
    Performs data aggregation for the GetWelderNameDetailsbyWorkOrderNumberandCriteria API.
    
    This function analyzes weld-level data, consolidates all welder fields (Welder1-4), 
    and aggregates total weld counts and category counts per unique welder. It also calculates
    the percentage distribution of workload among the unique welders with high precision.
    """
    total_weld_records = len(clean_data_array)
    
    # Use a dictionary to store aggregated welder data: {welder_id: {name: str, total: int, production: int, repaired: int, cutout: int}}
    welder_aggregator = defaultdict(lambda: {"name": "", "total_welds": 0, "Production": 0, "Repaired": 0, "CutOut": 0})
    
    # --- Step 1: Aggregate Data ---
    for record in clean_data_array:
        weld_category = record.get("WeldCategory", "Unknown")
        
        # Iterate through all four potential welder fields
        for i in range(1, 5):
            welder_field = record.get(f"Welder{i}")
            
            if welder_field and welder_field.strip() != "":
                # Welder format: "Name (ID)"
                if '(' in welder_field and ')' in welder_field:
                    try:
                        name_part, id_part = welder_field.split('(')
                        welder_name = name_part.strip()
                        welder_id = id_part.replace(')', '').strip()
                    except ValueError:
                        welder_name = welder_field
                        welder_id = "N/A"
                else:
                    welder_name = welder_field
                    welder_id = "N/A"
                    
                # Update the aggregator for this unique Welder ID
                welder_data = welder_aggregator[welder_id]
                welder_data["name"] = welder_name
                welder_data["id"] = welder_id
                welder_data["total_welds"] += 1
                
                if weld_category in ["Production", "Repaired", "CutOut"]:
                    welder_data[weld_category] += 1
                
    # --- Step 2: Finalize Results and Calculate Metrics ---
    
    aggregated_welder_list = [data for data in welder_aggregator.values() if data["id"] != "N/A"]
    total_unique_welders = len(aggregated_welder_list)
    
    # Helper to format distributions with two decimal places
    def get_distributions(counts, total):
        if total == 0: return {}
        return {
            item: {
                "count": count, 
                "percentage": round((count / total) * 100, 2) # <-- ROUNDED TO 2 DECIMAL PLACES
            }
            for item, count in counts.items()
        }

    # Calculate overall category distribution across all welds (based on raw weld records)
    overall_category_counts = defaultdict(int)
    for record in clean_data_array:
        category = record.get("WeldCategory", "Unknown")
        if category in ["Production", "Repaired", "CutOut"]:
            overall_category_counts[category] += 1

    # Calculate Welder Workload Distribution
    welder_workload_counts = {
        data['name']: data['total_welds'] for data in aggregated_welder_list
    }
    
    # The total number of unique welder appearances (sum of 'Total Welds') is used as the base.
    # IMPORTANT: We should use the total count of *welds themselves* (total_weld_records)
    # as the base for the overall workload distribution percentage.
    
    analysis_results = {
        "total_records": total_weld_records,
        "total_unique_welders": total_unique_welders,
        "raw_data": clean_data_array,
        "filter_applied": api_parameters,
        "aggregated_data": aggregated_welder_list,
        "counts": {
            "overall_weld_category_distribution": get_distributions(overall_category_counts, total_weld_records),
            "welder_workload_distribution": get_distributions(welder_workload_counts, total_weld_records),
        }
    }
    
    return analysis_results