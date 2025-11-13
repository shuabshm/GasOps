import logging
from collections import defaultdict
import statistics

logger = logging.getLogger(__name__)

def analyze_GetWeldsbyTRIndicationandWorkOrderNumber(clean_data_array, api_parameters):
    """
    Performs data analysis for the GetWeldsbyTRIndicationandWorkOrderNumber API.

    This function counts the total number of affected welds and analyzes the distribution
    of the IndicationCount to highlight severity and priority.
    """
    total_records = len(clean_data_array) # Total number of affected welds

    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,  # Full list of affected welds
        "filter_applied": api_parameters,
        "counts": {
            "weld_serial_number_distribution": defaultdict(int),
            "indication_distribution": defaultdict(int),
            "indication_count_distribution": defaultdict(int),
            "indication_count_stats": {} # Min, Max, Average
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis ---

    weld_serial_number_counts = analysis_results["counts"]["weld_serial_number_distribution"]
    indication_counts_dist = analysis_results["counts"]["indication_distribution"]
    count_of_counts = defaultdict(int) # Counts of the IndicationCount field (e.g., 5 welds had 2 indications)
    indication_counts = [] # List to hold all count values for mean/min/max

    for record in clean_data_array:
        # Count distributions for all fields
        weld_serial_number_counts[record.get("WeldSerialNumber", "Unknown")] += 1
        indication_counts_dist[record.get("Indication", "Unknown")] += 1

        try:
            # Note: The IndicationCount is returned as a string and must be converted to an integer
            count = int(record.get("IndicationCount", 0))
            if count > 0:
                count_of_counts[count] += 1
                indication_counts.append(count)
        except ValueError:
            logger.warning(f"Non-integer value found for IndicationCount: {record.get('IndicationCount')}")

    # Format the distributions with counts and percentages
    def get_distributions(counts):
        if total_records == 0: return {}
        return {
            item: {
                "count": count,
                "percentage": round((count / total_records) * 100, 2)
            }
            for item, count in counts.items()
        }

    analysis_results["counts"]["weld_serial_number_distribution"] = get_distributions(weld_serial_number_counts)
    analysis_results["counts"]["indication_distribution"] = get_distributions(indication_counts_dist)
    analysis_results["counts"]["indication_count_distribution"] = get_distributions(count_of_counts)

    # Calculate key statistics (Min, Max, Avg)
    if indication_counts:
        analysis_results["counts"]["indication_count_stats"] = {
            "total_indication_occurrences": sum(indication_counts),
            "min_count_per_weld": min(indication_counts),
            "max_count_per_weld": max(indication_counts),
            "average_count_per_weld": round(statistics.mean(indication_counts), 2)
        }

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_weld_serial_numbers": len(set(record.get("WeldSerialNumber") for record in clean_data_array if record.get("WeldSerialNumber"))),
        "total_distinct_indications": len(set(record.get("Indication") for record in clean_data_array if record.get("Indication") and record.get("Indication").strip())),
        "total_distinct_indication_counts": len(set(record.get("IndicationCount") for record in clean_data_array if record.get("IndicationCount")))
    }

    return analysis_results
