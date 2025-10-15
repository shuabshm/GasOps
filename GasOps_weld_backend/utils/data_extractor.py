import logging

logger = logging.getLogger(__name__)

def extract_clean_data(api_results):
    """
    Extracts clean data from a list of API responses by handling common nesting patterns.
    This function consolidates the data extraction logic to make it reusable and scalable.
    
    Args:
        api_results (list): A list of dictionaries, where each dictionary is an API result
                            with 'api_name', 'parameters', and 'data'.
                            
    Returns:
        list: A flattened list of the core data objects extracted from all API responses.
    """
    clean_data_list = []

    for api_result in api_results:
        if "error" in api_result:
            continue

        api_name = api_result.get("api_name", "Unknown")
        api_data = api_result.get("data", {})

        # Check for the primary, common nesting pattern used across your APIs
        data_container = api_data.get("data", {}).get("Data")

        # Fallback for simpler structures where data is at a top level "Data" key
        if data_container is None:
            data_container = api_data.get("Data")

        # Case 1: The extracted data is a list of records (most common case)
        if isinstance(data_container, list):
            clean_data_list.extend(data_container)
            logger.info(f"Extracted {len(data_container)} records from {api_name} API.")
        
        # Case 2: The extracted data is a single dictionary (e.g., GetDetailsbyWeldSerialNumber)
        elif isinstance(data_container, dict):
            clean_data_list.append(data_container)
            logger.info(f"Extracted a single nested object from {api_name} API.")

        else:
            logger.warning(f"Could not extract data from {api_name} API. Unexpected data type: {type(data_container)}")

    return clean_data_list