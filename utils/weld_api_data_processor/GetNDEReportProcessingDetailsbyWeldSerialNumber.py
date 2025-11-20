import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetNDEReportProcessingDetailsbyWeldSerialNumber(clean_data_array, api_parameters):
    """
    Performs data analysis and statistical calculations for the 
    GetNDEReportProcessingDetailsbyWeldSerialNumber API.
    
    CRITICAL: This function must handle the nested structure where data is 
    stored under keys (Report Type) within the main data object.
    
    The structure is: [ { "Conventional NDE": [ {}, {} ], "UT NDE": [ {} ] } ]
    
    It flattens the nested lists, counts records, and analyzes the technical parameters.
    """
    
    # 1. FLATTEN THE NESTED DATA (Crucial step for this API)
    
    # The clean_data_array should contain a single dictionary (the contents of the 'Data' field)
    if not clean_data_array or not isinstance(clean_data_array[0], dict):
        return {
            "total_records": 0,
            "raw_data": [],
            "filter_applied": api_parameters,
            "counts": {}
        }

    raw_nested_data = clean_data_array[0]
    flattened_reports = []
    
    for report_type, reports_list in raw_nested_data.items():
        if isinstance(reports_list, list):
            for report in reports_list:
                # Add the report type to the record for easier analysis later
                report['ReportTypeKey'] = report_type 
                flattened_reports.append(report)
        else:
            logger.warning(f"Unexpected non-list value found under report key: {report_type}")

    total_records = len(flattened_reports)
    
    analysis_results = {
        "total_records": total_records,
        "raw_data": flattened_reports,  # The flattened list of all reports
        "filter_applied": api_parameters,
        "counts": {
            "report_type_key_distribution": {},
            "report_type_distribution": {},
            "inspector_distribution": {},
            "nde_report_number_distribution": {},
            "date_radiographed_distribution": {}
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Perform statistical analysis on the flattened data ---

    report_type_key_counts = defaultdict(int)
    report_type_counts = defaultdict(int)
    inspector_counts = defaultdict(int)
    nde_report_number_counts = defaultdict(int)
    date_radiographed_counts = defaultdict(int)

    for record in flattened_reports:
        # We use the key we added during flattening
        report_type_key_counts[record.get("ReportTypeKey", "Unknown")] += 1
        report_type_counts[record.get("ReportType", "Unknown")] += 1
        inspector_counts[record.get("NDEName", "Unknown")] += 1
        nde_report_number_counts[record.get("NDEReportNumber", "Unknown")] += 1
        date_radiographed_counts[record.get("DateRadiographed", "Unknown")] += 1
        
    # Format the distributions with counts and percentages
    def get_distributions(counts):
        # Calculate distributions only if total_records > 0
        if total_records == 0: return {}
        return {
            item: {"count": count, "percentage": (count / total_records) * 100}
            for item, count in counts.items()
        }

    analysis_results["counts"]["report_type_key_distribution"] = get_distributions(report_type_key_counts)
    analysis_results["counts"]["report_type_distribution"] = get_distributions(report_type_counts)
    analysis_results["counts"]["inspector_distribution"] = get_distributions(inspector_counts)
    analysis_results["counts"]["nde_report_number_distribution"] = get_distributions(nde_report_number_counts)
    analysis_results["counts"]["date_radiographed_distribution"] = get_distributions(date_radiographed_counts)

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_nde_report_numbers": len(set(record.get("NDEReportNumber") for record in flattened_reports if record.get("NDEReportNumber") and record.get("NDEReportNumber").strip())),
        "total_distinct_weld_serial_numbers": len(set(record.get("WeldSerialNumber") for record in flattened_reports if record.get("WeldSerialNumber"))),
        "total_distinct_report_type_keys": len(set(record.get("ReportTypeKey") for record in flattened_reports if record.get("ReportTypeKey"))),
        "total_distinct_report_types": len(set(record.get("ReportType") for record in flattened_reports if record.get("ReportType"))),
        "total_distinct_inspectors": len(set(record.get("NDEName") for record in flattened_reports if record.get("NDEName") and record.get("NDEName").strip())),
        "total_distinct_dates_radiographed": len(set(record.get("DateRadiographed") for record in flattened_reports if record.get("DateRadiographed")))
    }

    # Optional: Calculate range/average for key technical fields
    try:
        exposure_times = [float(r.get("ExposureTime")) for r in flattened_reports if r.get("ExposureTime") not in ["", None]]
        if exposure_times:
            analysis_results["counts"]["exposure_stats"] = {
                "min": min(exposure_times),
                "max": max(exposure_times),
                "avg": sum(exposure_times) / len(exposure_times)
            }
    except Exception as e:
        logger.warning(f"Error calculating exposure stats: {e}")

    return analysis_results
