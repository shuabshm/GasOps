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
            # 1. Inspection Results
            "cwi_result_distribution": defaultdict(int),
            "nde_result_distribution": defaultdict(int),
            "cri_result_distribution": defaultdict(int),
            "tr_result_distribution": defaultdict(int),

            # 2. Weld Characteristics
            "welder_distribution": defaultdict(int),
            "weld_category_distribution": defaultdict(int),
            "tiein_weld_distribution": defaultdict(int),
            "prefab_distribution": defaultdict(int),
            "gap_distribution": defaultdict(int),
            "weld_unlocked_distribution": defaultdict(int),
            "added_to_map_distribution": defaultdict(int),

            # 3. Rod Class Usage
            "root_rod_class_distribution": defaultdict(int),
            "filler_rod_class_distribution": defaultdict(int),
            "hot_rod_class_distribution": defaultdict(int),
            "cap_rod_class_distribution": defaultdict(int),

            # 4. Identifiers
            "weld_serial_number_distribution": defaultdict(int),
            "project_number_distribution": defaultdict(int),
            "heat_serial_number1_distribution": defaultdict(int),
            "heat_serial_number2_distribution": defaultdict(int),

            # 5. Inspector Names
            "cwi_name_distribution": defaultdict(int),
            "nde_report_number_distribution": defaultdict(int),
            "nde_name_distribution": defaultdict(int),
            "cri_name_distribution": defaultdict(int),
            "tr_name_distribution": defaultdict(int)
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
        counts["gap_distribution"][record.get("Gap", "N/A")] += 1
        counts["weld_unlocked_distribution"][record.get("WeldUnlocked", "N/A")] += 1
        counts["added_to_map_distribution"][record.get("AddedtoWeldMap", "N/A")] += 1

        # 3. Rod Class Usage
        counts["root_rod_class_distribution"][record.get("RootRodClass", "N/A")] += 1
        counts["filler_rod_class_distribution"][record.get("FillerRodClass", "N/A")] += 1
        counts["hot_rod_class_distribution"][record.get("HotRodClass", "N/A")] += 1
        counts["cap_rod_class_distribution"][record.get("CapRodClass", "N/A")] += 1

        # 4. Identifiers
        counts["weld_serial_number_distribution"][record.get("WeldSerialNumber", "Unknown")] += 1
        counts["project_number_distribution"][record.get("ProjectNumber", "Unknown")] += 1
        counts["heat_serial_number1_distribution"][record.get("HeatSerialNumber1", "Unknown")] += 1
        counts["heat_serial_number2_distribution"][record.get("HeatSerialNumber2", "Unknown")] += 1

        # 5. Inspector Names
        counts["cwi_name_distribution"][record.get("CWIName", "Unknown")] += 1
        counts["nde_report_number_distribution"][record.get("NDEReportNumber", "Unknown")] += 1
        counts["nde_name_distribution"][record.get("NDEName", "Unknown")] += 1
        counts["cri_name_distribution"][record.get("CRIName", "Unknown")] += 1
        counts["tr_name_distribution"][record.get("TRName", "Unknown")] += 1

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

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_weld_serial_numbers": len(set(record.get("WeldSerialNumber") for record in clean_data_array if record.get("WeldSerialNumber"))),
        "total_distinct_project_numbers": len(set(record.get("ProjectNumber") for record in clean_data_array if record.get("ProjectNumber"))),
        "total_distinct_weld_categories": len(set(record.get("WeldCategory") for record in clean_data_array if record.get("WeldCategory"))),
        "total_distinct_tiein_weld": len(set(record.get("TieinWeld") for record in clean_data_array if record.get("TieinWeld"))),
        "total_distinct_prefab": len(set(record.get("Prefab") for record in clean_data_array if record.get("Prefab"))),
        "total_distinct_gap": len(set(record.get("Gap") for record in clean_data_array if record.get("Gap"))),
        "total_distinct_heat_serial_number1": len(set(record.get("HeatSerialNumber1") for record in clean_data_array if record.get("HeatSerialNumber1"))),
        "total_distinct_heat_serial_number2": len(set(record.get("HeatSerialNumber2") for record in clean_data_array if record.get("HeatSerialNumber2"))),
        "total_distinct_root_rod_class": len(set(record.get("RootRodClass") for record in clean_data_array if record.get("RootRodClass"))),
        "total_distinct_filler_rod_class": len(set(record.get("FillerRodClass") for record in clean_data_array if record.get("FillerRodClass"))),
        "total_distinct_hot_rod_class": len(set(record.get("HotRodClass") for record in clean_data_array if record.get("HotRodClass"))),
        "total_distinct_cap_rod_class": len(set(record.get("CapRodClass") for record in clean_data_array if record.get("CapRodClass"))),
        "total_distinct_weld_unlocked": len(set(record.get("WeldUnlocked") for record in clean_data_array if record.get("WeldUnlocked"))),
        "total_distinct_added_to_weld_map": len(set(record.get("AddedtoWeldMap") for record in clean_data_array if record.get("AddedtoWeldMap"))),
        "total_distinct_welders": len(set(record.get(f"Welder{i}") for record in clean_data_array for i in range(1, 5) if record.get(f"Welder{i}") and record.get(f"Welder{i}").strip())),
        "total_distinct_cwi_names": len(set(record.get("CWIName") for record in clean_data_array if record.get("CWIName") and record.get("CWIName").strip())),
        "total_distinct_cwi_results": len(set(record.get("CWIResult") for record in clean_data_array if record.get("CWIResult") and record.get("CWIResult").strip())),
        "total_distinct_nde_report_numbers": len(set(record.get("NDEReportNumber") for record in clean_data_array if record.get("NDEReportNumber") and record.get("NDEReportNumber").strip())),
        "total_distinct_nde_names": len(set(record.get("NDEName") for record in clean_data_array if record.get("NDEName") and record.get("NDEName").strip())),
        "total_distinct_nde_results": len(set(record.get("NDEResult") for record in clean_data_array if record.get("NDEResult") and record.get("NDEResult").strip())),
        "total_distinct_cri_names": len(set(record.get("CRIName") for record in clean_data_array if record.get("CRIName") and record.get("CRIName").strip())),
        "total_distinct_cri_results": len(set(record.get("CRIResult") for record in clean_data_array if record.get("CRIResult") and record.get("CRIResult").strip())),
        "total_distinct_tr_names": len(set(record.get("TRName") for record in clean_data_array if record.get("TRName") and record.get("TRName").strip())),
        "total_distinct_tr_results": len(set(record.get("TRResult") for record in clean_data_array if record.get("TRResult") and record.get("TRResult").strip()))
    }

    return analysis_results
