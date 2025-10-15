import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def analyze_GetDetailsbyWeldSerialNumber(clean_data_array, api_parameters):
    """
    Performs data analysis for the GetDetailsbyWeldSerialNumber API.
    
    This API returns a single record with nested sections (Overall Details, Asset Details, 
    CWI/NDE Result Details, NDE Report Film Details). The function ensures data is structured
    and calculates metrics only on the list-based section (Film Details).
    """
    # This API always returns a list containing a single, complex dictionary (the weld details)
    if not clean_data_array or not isinstance(clean_data_array[0], dict):
        return {
            "total_records": 0,
            "raw_data": [],
            "filter_applied": api_parameters,
            "counts": {}
        }

    # The entire complex object for the single weld is the record we analyze
    weld_detail_object = clean_data_array[0]
    
    # The only section containing a list of items is 'NDE Report Film Details'
    film_details = weld_detail_object.get("NDE Report Film Details", [])
    film_detail_count = len(film_details)
    
    analysis_results = {
        # Total records is 1 (the single weld object)
        "total_records": 1, 
        # Pass the entire complex object as raw data
        "raw_data": weld_detail_object, 
        "filter_applied": api_parameters,
        "counts": {
            "film_detail_count": film_detail_count,
            "indication_distribution": {}
        }
    }

    # --- Perform statistical analysis on the nested film details ---
    if film_detail_count > 0:
        # Tally NDE Indications found across all clock positions
        indication_counts = defaultdict(int)
        
        for film_record in film_details:
            # Assuming NDEIndications is a comma-separated string or list (we'll process it as a string)
            indications_str = film_record.get("NDEIndications")
            if indications_str:
                # Basic normalization/splitting
                indications = [ind.strip() for ind in indications_str.split(',') if ind.strip()]
                for ind in indications:
                    indication_counts[ind] += 1
        
        # Calculate distributions for the indications found
        def get_distributions(counts, total):
            if total == 0: return {}
            return {
                item: {"count": count, "percentage": (count / total) * 100}
                for item, count in counts.items()
            }
            
        total_indications = sum(indication_counts.values())
        analysis_results["counts"]["indication_distribution"] = get_distributions(
            indication_counts, total_indications
        )
        analysis_results["counts"]["total_indications_found"] = total_indications
        
    return analysis_results
