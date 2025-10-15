import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetWeldDetailsbyWorkOrderNumberandCriteria(clean_data_array, api_parameters):
    """
    Performs comprehensive data analysis for the GetWeldDetailsbyWorkOrderNumberandCriteria API.
    
    This function counts total records and analyzes distributions for all four inspection 
    levels, welder assignments, rod class usage, and key weld characteristics.
    """
    total_records = len(clean_data_array)
    
    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,
        "filter_applied": api_parameters,
        "counts": {
            # 1. Inspection Results (Already done)
            "cwi_result_distribution": defaultdict(int),
            "nde_result_distribution": defaultdict(int),
            "cri_result_distribution": defaultdict(int),
            "tr_result_distribution": defaultdict(int),
            
            # 2. Weld Characteristics (Updated/New)
            "welder_distribution": defaultdict(int),
            "weld_category_distribution": defaultdict(int),
            "tiein_weld_distribution": defaultdict(int),    # <-- NEW
            "prefab_distribution": defaultdict(int),        # <-- NEW
            "weld_unlocked_distribution": defaultdict(int), # <-- NEW
            "added_to_map_distribution": defaultdict(int),  # <-- NEW
            
            # 3. Rod Class Usage (New)
            "root_rod_class_distribution": defaultdict(int), # <-- NEW
            "filler_rod_class_distribution": defaultdict(int), # <-- NEW
            "hot_rod_class_distribution": defaultdict(int), # <-- NEW
            "cap_rod_class_distribution": defaultdict(int), # <-- NEW

            # 4. Material/Heat Descriptions (New)
            "heat1_description_distribution": defaultdict(int), # <-- NEW
            "heat2_description_distribution": defaultdict(int)  # <-- NEW
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Setup Counts ---
    counts = analysis_results["counts"]
    
    # --- Perform statistical analysis ---
    for record in clean_data_array:
        # 1. Inspection Results
        counts["cwi_result_distribution"][record.get("CWIResult", "N/A")] += 1
        counts["nde_result_distribution"][record.get("NDEResult", "N/A")] += 1
        counts["cri_result_distribution"][record.get("CRIResult", "N/A")] += 1
        counts["tr_result_distribution"][record.get("TRResult", "N/A")] += 1
        
        # 2. Weld Characteristics
        counts["weld_category_distribution"][record.get("WeldCategory", "Unknown")] += 1
        counts["tiein_weld_distribution"][record.get("TieinWeld", "N/A")] += 1
        counts["prefab_distribution"][record.get("Prefab", "N/A")] += 1
        counts["weld_unlocked_distribution"][record.get("WeldUnlocked", "N/A")] += 1
        counts["added_to_map_distribution"][record.get("AddedtoWeldMap", "N/A")] += 1

        # 3. Rod Class Usage
        counts["root_rod_class_distribution"][record.get("RootRodClass", "N/A")] += 1
        counts["filler_rod_class_distribution"][record.get("FillerRodClass", "N/A")] += 1
        counts["hot_rod_class_distribution"][record.get("HotRodClass", "N/A")] += 1
        counts["cap_rod_class_distribution"][record.get("CapRodClass", "N/A")] += 1

        # 4. Material/Heat Descriptions
        counts["heat1_description_distribution"][record.get("Heat1Description", "N/A")] += 1
        counts["heat2_description_distribution"][record.get("Heat2Description", "N/A")] += 1
        
        # Welder Consolidation (Tally every welder mentioned across all four fields)
        for i in range(1, 5):
            welder_field = record.get(f"Welder{i}")
            if welder_field and welder_field.strip() != "":
                welder_name = welder_field.split('(')[0].strip()
                counts["welder_distribution"][welder_name] += 1
        
    # Format the distributions with counts and percentages
    def get_distributions(counts):
        if total_records == 0: return {}
        return {
            item: {"count": count, "percentage": (count / total_records) * 100}
            for item, count in counts.items()
        }

    # Finalize all distributions
    for key in analysis_results["counts"]:
        # Only process dictionaries (the defaultdict objects)
        if isinstance(analysis_results["counts"][key], defaultdict): 
            analysis_results["counts"][key] = get_distributions(analysis_results["counts"][key])
    
    return analysis_results
