import logging

logger = logging.getLogger(__name__)

def analyze_GetWorkOrdersbyWelderName(clean_data_array, api_parameters):
    """
    Performs data preprocessing and analytics for the GetWorkOrdersbyWelderName API.

    This function analyzes work order-level data for a specific welder,
    truncates long WeldSerialNumbers lists, and calculates aggregate statistics.

    Args:
        clean_data_array (list): List of work order records for the welder
        api_parameters (dict): API filter parameters (WelderName)

    Returns:
        dict: Enriched data with analytics and processed records
    """
    total_records = len(clean_data_array)

    if total_records == 0:
        logger.info("No work orders found for the given welder")
        return {
            "total_records": 0,
            "raw_data": [],
            "filter_applied": api_parameters,
            "total_welds": 0,
            "work_order_with_most_welds": None,
            "max_welds_count": 0,
            "welder_full_name": None,
            "welder_name_queried": api_parameters.get("WelderName", "Unknown"),
            "processed_records": []
        }

    # Initialize analytics
    total_welds = 0
    max_welds_count = 0
    work_order_with_most_welds = None
    welder_full_name = None

    # Process each work order record
    processed_records = []
    for record in clean_data_array:
        weld_count = record.get("WeldCount", 0)
        work_order_number = record.get("WorkOrderNumber", "N/A")
        weld_serial_numbers = record.get("WeldSerialNumbers", "")

        # Update analytics
        total_welds += weld_count

        if weld_count > max_welds_count:
            max_welds_count = weld_count
            work_order_with_most_welds = work_order_number

        # Capture full welder name from the first record
        if welder_full_name is None:
            welder_full_name = record.get("WelderName", api_parameters.get("WelderName", "Unknown"))

        # Truncate WeldSerialNumbers for display
        truncated_weld_serials = _truncate_weld_serial_numbers(weld_serial_numbers, weld_count)

        # Create processed record
        processed_record = {
            "WorkOrderNumber": work_order_number,
            "ProjectNumber": record.get("ProjectNumber", "N/A"),
            "WelderName": record.get("WelderName", "N/A"),
            "WelderITSID": record.get("WelderITSID", "N/A"),
            "WeldCount": weld_count,
            "WeldSerialNumbers_Truncated": truncated_weld_serials,
            "WeldSerialNumbers_Full": weld_serial_numbers  # Keep full list for reference
        }

        processed_records.append(processed_record)

    # Sort by WeldCount descending (most active work orders first)
    processed_records.sort(key=lambda x: x["WeldCount"], reverse=True)

    # Return enriched data with analytics
    return {
        "total_records": total_records,
        "raw_data": clean_data_array,  # Original data from API
        "filter_applied": api_parameters,
        "total_welds": total_welds,
        "work_order_with_most_welds": work_order_with_most_welds,
        "max_welds_count": max_welds_count,
        "welder_full_name": welder_full_name,
        "welder_name_queried": api_parameters.get("WelderName", "Unknown"),
        "processed_records": processed_records
    }


def _truncate_weld_serial_numbers(weld_serials_str, weld_count, max_display=3):
    """
    Truncates the WeldSerialNumbers string to show only first few entries plus total count.

    Args:
        weld_serials_str (str): Semicolon-separated weld serial numbers
        weld_count (int): Total count of welds
        max_display (int): Maximum number of weld serials to display before truncating

    Returns:
        str: Truncated string in format "240248; 240250; 240251... (150 total)"
    """
    if not weld_serials_str or weld_serials_str.strip() == "":
        return "-"

    # Split by semicolon and clean up
    weld_serials = [s.strip() for s in weld_serials_str.split(';') if s.strip()]

    if len(weld_serials) <= max_display:
        # No need to truncate
        return weld_serials_str

    # Take first max_display entries
    displayed_serials = weld_serials[:max_display]
    truncated = "; ".join(displayed_serials) + f"... ({weld_count} total)"

    return truncated
