import logging
from collections import Counter

logger = logging.getLogger(__name__)

def transform_weld_map_data(clean_data_array, api_parameters=None):
    """
    Transform weld map data to show only relevant columns and calculate statistics.
    
    Args:
        clean_data_array (list): Raw weld data from API
        api_parameters (dict): API filter parameters
        
    Returns:
        dict: Transformed data with weld map statistics
    """
    if api_parameters is None:
        api_parameters = {}
        
    logger.info(f"Transforming weld map data for {len(clean_data_array)} records")
    
    # Filter and transform records to only show required columns
    weld_map_records = []
    unique_welds = set()
    added_to_map_yes = 0
    added_to_map_no = 0
    
    for record in clean_data_array:
        if not isinstance(record, dict):
            continue
            
        # Extract required fields only
        weld_serial = record.get("WeldSerialNumber")
        added_to_map = record.get("AddedtoWeldMap", "")
        
        # Track unique welds
        if weld_serial:
            unique_welds.add(weld_serial)
            
        # Count AddedtoWeldMap status
        if added_to_map == "Yes":
            added_to_map_yes += 1
        elif added_to_map == "No":
            added_to_map_no += 1
            
        # Consolidate welders
        welders = []
        for i in range(1, 5):
            welder = record.get(f"Welder{i}")
            if welder:
                welders.append(welder)
        welders_str = ", ".join(welders) if welders else "-"
        
        weld_map_records.append({
            "ProjectNumber": record.get("ProjectNumber", "-"),
            "WeldCategory": record.get("WeldCategory", "-"),
            "WeldSerialNumber": weld_serial or "-",
            "AddedtoWeldMap": added_to_map or "-",
            "Welders": welders_str,
            "CWIName": record.get("CWIName", "-"),
            "CWIResult": record.get("CWIResult", "-"),
            "CWICompletionDate": record.get("CWICompletionDate", "-"),
            "NDEName": record.get("NDEName", "-"),
            "NDEResult": record.get("NDEResult", "-"),
            "NDECompletionDate": record.get("NDECompletionDate", "-"),
            "CRIName": record.get("CRIName", "-"),
            "CRIResult": record.get("CRIResult", "-"),
            "CRICompletionDate": record.get("CRICompletionDate", "-"),
            "TRName": record.get("TRName", "-"),
            "TRResult": record.get("TRResult", "-"),
            "TRCompletionDate": record.get("TRCompletionDate", "-")
        })
    
    # Calculate statistics
    total_unique_welds = len(unique_welds)
    
    logger.info(f"Weld map statistics: {total_unique_welds} unique welds, "
                f"{added_to_map_yes} added to map, {added_to_map_no} not added")
    
    return {
        "total_records": len(weld_map_records),
        "total_unique_welds": total_unique_welds,
        "added_to_map_yes": added_to_map_yes,
        "added_to_map_no": added_to_map_no,
        "weld_map_records": weld_map_records,
        "raw_data": clean_data_array,  # ADD THIS LINE - it was missing!
        "filter_applied": api_parameters,
        "is_weld_map_query": True,
        "counts": {},  # ADD THIS LINE - required by the prompt builder
        "distinct_counts": {}  # ADD THIS LINE - required by the prompt builder
    }