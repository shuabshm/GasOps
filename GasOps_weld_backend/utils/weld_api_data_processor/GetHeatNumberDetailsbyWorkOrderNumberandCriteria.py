import logging
from collections import defaultdict
import json
def analyze_GetHeatNumberDetailsbyWorkOrderNumberandCriteria(clean_data_array, api_parameters):
    """
    Performs data analysis and statistical calculations for the 
    GetHeatNumberDetailsbyWorkOrderNumberandCriteria API.
    
    This function counts records, calculates distributions, and prepares the data for AI summarization.
    It removes the burden of calculation from the LLM, ensuring accuracy.
    """
    total_records = len(clean_data_array)
    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,  # Pass the entire clean data array
        "filter_applied": api_parameters,
        "counts": {},
        "insights": []
    }

    if total_records == 0:
        return analysis_results

    # --- Perform all statistical analysis here ---
    
    # Analyze distributions for key fields based on the API schema
    asset_counts = defaultdict(int)
    material_counts = defaultdict(int)
    manufacturer_counts = defaultdict(int)
    
    for record in clean_data_array:
        asset_counts[record.get("Asset", "Unknown")] += 1
        material_counts[record.get("Material", "Unknown")] += 1
        manufacturer_counts[record.get("Manufacturer", "Unknown")] += 1

    # Format the distributions with counts and percentages
    def get_distributions(counts):
        return {
            item: {"count": count, "percentage": (count / total_records) * 100}
            for item, count in counts.items()
        }

    analysis_results["counts"]["asset_distribution"] = get_distributions(asset_counts)
    analysis_results["counts"]["material_distribution"] = get_distributions(material_counts)
    analysis_results["counts"]["manufacturer_distribution"] = get_distributions(manufacturer_counts)

    return analysis_results