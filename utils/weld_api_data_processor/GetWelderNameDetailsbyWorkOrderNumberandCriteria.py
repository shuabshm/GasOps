import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetWelderNameDetailsbyWorkOrderNumberandCriteria(clean_data_array, api_parameters):
    """
    Performs data aggregation for the GetWelderNameDetailsbyWorkOrderNumberandCriteria API.

    This function analyzes weld-level data, consolidates all welder fields (Welder1-4),
    and aggregates total weld counts and category counts per unique welder. It also calculates
    the percentage distribution of workload among the unique welders with high precision.

    CRITICAL: Counts unique welds per welder, not total appearances. If a welder appears in
    multiple Welder1-4 positions for the SAME weld, it only counts as 1 weld.
    """
    total_weld_records = len(clean_data_array)

    # Use a dictionary to store aggregated welder data with sets to track unique welds
    # {welder_id: {name: str, weld_serials: set, production_serials: set, repaired_serials: set, cutout_serials: set}}
    welder_aggregator = defaultdict(lambda: {
        "name": "",
        "weld_serials": set(),
        "production_serials": set(),
        "repaired_serials": set(),
        "cutout_serials": set()
    })

    # --- Step 1: Aggregate Data with Unique Weld Tracking ---
    for record in clean_data_array:
        weld_serial = record.get("WeldSerialNumber", "")
        weld_category = record.get("WeldCategory", "Unknown")

        # Track welders who worked on this specific weld (to avoid duplicate counting if same welder in multiple positions)
        welders_on_this_weld = set()

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

                # Skip if we already processed this welder for this weld
                if welder_id in welders_on_this_weld:
                    continue

                welders_on_this_weld.add(welder_id)

                # Update the aggregator for this unique Welder ID
                welder_data = welder_aggregator[welder_id]
                welder_data["name"] = welder_name
                welder_data["id"] = welder_id

                # Add this weld serial to the welder's set of unique welds
                if weld_serial:
                    welder_data["weld_serials"].add(weld_serial)

                    # Track category-specific weld serials
                    if weld_category == "Production":
                        welder_data["production_serials"].add(weld_serial)
                    elif weld_category == "Repaired":
                        welder_data["repaired_serials"].add(weld_serial)
                    elif weld_category == "CutOut":
                        welder_data["cutout_serials"].add(weld_serial)
                
    # --- Step 2: Convert Sets to Counts and Finalize Results ---

    # Convert the sets to counts for final output
    for welder_id, welder_data in welder_aggregator.items():
        welder_data["total_welds"] = len(welder_data["weld_serials"])
        welder_data["Production"] = len(welder_data["production_serials"])
        welder_data["Repaired"] = len(welder_data["repaired_serials"])
        welder_data["CutOut"] = len(welder_data["cutout_serials"])

        # Remove the sets from final output (keep only counts)
        del welder_data["weld_serials"]
        del welder_data["production_serials"]
        del welder_data["repaired_serials"]
        del welder_data["cutout_serials"]

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
    
    # Calculate Weld Serial Number Distribution
    weld_serial_number_counts = defaultdict(int)
    for record in clean_data_array:
        weld_serial_number_counts[record.get("WeldSerialNumber", "Unknown")] += 1

    analysis_results = {
        "total_records": total_weld_records,
        "total_unique_welders": total_unique_welders,
        "raw_data": clean_data_array,
        "filter_applied": api_parameters,
        "aggregated_data": aggregated_welder_list,
        "counts": {
            "overall_weld_category_distribution": get_distributions(overall_category_counts, total_weld_records),
            "welder_workload_distribution": get_distributions(welder_workload_counts, total_weld_records),
            "weld_serial_number_distribution": get_distributions(weld_serial_number_counts, total_weld_records)
        }
    }

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_weld_serial_numbers": len(set(record.get("WeldSerialNumber") for record in clean_data_array if record.get("WeldSerialNumber"))),
        "total_distinct_weld_categories": len(set(record.get("WeldCategory") for record in clean_data_array if record.get("WeldCategory"))),
        # Use the already-aggregated welder count, which properly filters out N/A and empty entries
        "total_distinct_welders": total_unique_welders
    }

    return analysis_results