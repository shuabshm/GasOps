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
    heat_number_counts = defaultdict(int)
    asset_counts = defaultdict(int)
    asset_subcategory_counts = defaultdict(int)
    material_counts = defaultdict(int)
    manufacturer_counts = defaultdict(int)

    for record in clean_data_array:
        heat_number_counts[record.get("HeatNumber", "Unknown")] += 1
        asset_counts[record.get("Asset", "Unknown")] += 1
        asset_subcategory_counts[record.get("AssetSubcategory", "Unknown")] += 1
        material_counts[record.get("Material", "Unknown")] += 1
        manufacturer_counts[record.get("Manufacturer", "Unknown")] += 1

    # Format the distributions with counts and percentages
    def get_distributions(counts):
        return {
            item: {"count": count, "percentage": (count / total_records) * 100}
            for item, count in counts.items()
        }

    analysis_results["counts"]["heat_number_distribution"] = get_distributions(heat_number_counts)
    analysis_results["counts"]["asset_distribution"] = get_distributions(asset_counts)
    analysis_results["counts"]["asset_subcategory_distribution"] = get_distributions(asset_subcategory_counts)
    analysis_results["counts"]["material_distribution"] = get_distributions(material_counts)
    analysis_results["counts"]["manufacturer_distribution"] = get_distributions(manufacturer_counts)

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_heat_numbers": len(set(record.get("HeatNumber") for record in clean_data_array if record.get("HeatNumber"))),
        "total_distinct_assets": len(set(record.get("Asset") for record in clean_data_array if record.get("Asset"))),
        "total_distinct_asset_subcategories": len(set(record.get("AssetSubcategory") for record in clean_data_array if record.get("AssetSubcategory") and record.get("AssetSubcategory").strip())),
        "total_distinct_materials": len(set(record.get("Material") for record in clean_data_array if record.get("Material") and record.get("Material").strip())),
        "total_distinct_manufacturers": len(set(record.get("Manufacturer") for record in clean_data_array if record.get("Manufacturer") and record.get("Manufacturer").strip()))
    }

    return analysis_results