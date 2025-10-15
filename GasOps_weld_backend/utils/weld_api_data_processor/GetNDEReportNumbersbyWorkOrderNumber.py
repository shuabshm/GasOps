import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetNDEReportNumbersbyWorkOrderNumber(clean_data_array, api_parameters):
    """
    Performs data analysis and statistical calculations for the 
    GetNDEReportNumbersbyWorkOrderNumber API.
    
    This function counts records and determines the distribution of NDE Report Types.
    """
    total_records = len(clean_data_array)
    
    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,  # Full list of NDE reports
        "filter_applied": api_parameters,
        "counts": {
            "report_type_distribution": {}
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis on report types ---
    
    report_type_counts = defaultdict(int)
    
    for record in clean_data_array:
        report_type_counts[record.get("ReportType", "Unknown")] += 1

    # Format the distributions with counts and percentages
    def get_distributions(counts):
        # Calculate distributions only if total_records > 0
        if total_records == 0: return {}
        return {
            item: {"count": count, "percentage": (count / total_records) * 100}
            for item, count in counts.items()
        }

    analysis_results["counts"]["report_type_distribution"] = get_distributions(report_type_counts)
    
    return analysis_results
