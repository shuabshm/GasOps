import logging
from collections import defaultdict
import statistics
import datetime
from dateutil import parser

logger = logging.getLogger(__name__)

def analyze_GetWorkOrderInformation(clean_data_array, api_parameters):
    """
    Performs comprehensive data analysis for the GetWorkOrderInformation API.
    
    This function analyzes distributions across all available geographical, status, 
    and personnel fields. It consolidates multiple personnel fields (e.g., Engineer1-4)
    into single distribution metrics and tracks all individual fields for maximum coverage.
    """
    total_records = len(clean_data_array)
    
    analysis_results = {
        "total_records": total_records,
        "raw_data": clean_data_array,
        "filter_applied": api_parameters,
        "counts": {
            # Identifiers
            "work_order_number_distribution": defaultdict(int),
            "project_number_distribution": defaultdict(int),

            # Core Distributions
            "region_name_distribution": defaultdict(int),
            "work_order_status_distribution": defaultdict(int),
            "crew_distribution": defaultdict(int),
            "is_redig_distribution": defaultdict(int),
            "created_on_date_distribution": defaultdict(int),

            # Contractor Info
            "contractor_name_distribution": defaultdict(int),
            "contractor_cwi_name_distribution": defaultdict(int),
            "contractor_nde_name_distribution": defaultdict(int),
            "contractor_cri_name_distribution": defaultdict(int),

            # Personnel Distributions (Consolidated)
            "manager_distribution": defaultdict(int),
            "supervisor_distribution": defaultdict(int),
            "engineer_distribution": defaultdict(int),
            "records_support_distribution": defaultdict(int),

            # Temporal Stats
            "date_stats": {}
        }
    }

    if total_records == 0:
        return analysis_results

    # --- Setup Counts and Date Tracking ---
    counts = analysis_results["counts"]
    created_dates = []

    # Helper for processing multi-field personnel (Engineers, Supervisors, etc.)
    def process_personnel(record, prefix, target_dict):
        # Handle fields like Engineer1, Engineer2, etc. (up to 4, based on pattern)
        found_multi_field = False
        for i in range(1, 5): 
            person_field = record.get(f"{prefix}{i}")
            if person_field and person_field.strip() != "":
                person_name = person_field.split('(')[0].strip()
                target_dict[person_name] += 1
                found_multi_field = True
        return found_multi_field
                
    # --- Perform Statistical Analysis ---
    for record in clean_data_array:
        # Identifiers
        counts["work_order_number_distribution"][record.get("WorkOrderNumber", "Unknown")] += 1
        counts["project_number_distribution"][record.get("ProjectNumber", "Unknown")] += 1

        # Core Distributions
        counts["region_name_distribution"][record.get("RegionName", "Unknown")] += 1
        counts["work_order_status_distribution"][record.get("WorkOrderStatusDescription", "Unknown")] += 1
        counts["crew_distribution"][record.get("Crew", "Unknown")] += 1
        counts["is_redig_distribution"][record.get("IsRedig", "Unknown")] += 1
        counts["created_on_date_distribution"][record.get("CreatedOnDate", "Unknown")] += 1

        # Contractor Info
        counts["contractor_name_distribution"][record.get("ContractorName", "Unknown")] += 1
        counts["contractor_cwi_name_distribution"][record.get("ContractorCWIName", "Unknown")] += 1
        counts["contractor_nde_name_distribution"][record.get("ContractorNDEName", "Unknown")] += 1
        counts["contractor_cri_name_distribution"][record.get("ContractorCRIName", "Unknown")] += 1

        # Single Personnel Fields
        counts["records_support_distribution"][record.get("RecordsSupport", "Unknown")] += 1

        # Consolidated Personnel (Manager, Supervisors, Engineers)
        # Process Manager field (single field, not multi)
        manager = record.get("Manager")
        if manager and manager.strip() != "":
            counts["manager_distribution"][manager.strip()] += 1

        # Process Supervisor1-4 fields
        process_personnel(record, "Supervisor", counts["supervisor_distribution"])

        # Process Engineer1-4 fields
        process_personnel(record, "Engineer", counts["engineer_distribution"])
        
        # Temporal Analysis: Parse the date string for min/max
        created_date_str = record.get("CreatedOnDate")
        if created_date_str:
            try:
                # Assuming date is in ISO format like '2025-10-15T03:38:07Z'
                # We store the datetime object for accurate comparison
                created_dates.append(parser.parse(created_date_str).date())
            except Exception as e:
                logger.debug(f"Could not parse date string '{created_date_str}': {e}")


    # Format the distributions with counts and percentages (rounded to 2 decimal places)
    def get_distributions(counts):
        if total_records == 0: return {}
        return {
            item: {
                "count": count, 
                "percentage": round((count / total_records) * 100, 2)
            }
            for item, count in counts.items()
        }

    # Finalize all distributions
    for key in counts.keys():
        if isinstance(counts[key], defaultdict):
            # Only process if the dictionary contains actual data (not just "N/A" unless relevant)
            if any(k != "N/A" for k in counts[key].keys()):
                counts[key] = get_distributions(counts[key])
            else:
                counts[key] = {} # Clear empty distributions
            
    # Finalize Temporal Stats
    if created_dates:
        # Find min/max dates accurately using datetime objects
        counts["date_stats"]["earliest_created_date"] = min(created_dates).isoformat()
        counts["date_stats"]["latest_created_date"] = max(created_dates).isoformat()

    # Add distinct counts for ALL fields
    analysis_results["distinct_counts"] = {
        "total_distinct_work_order_numbers": len(set(record.get("WorkOrderNumber") for record in clean_data_array if record.get("WorkOrderNumber"))),
        "total_distinct_project_numbers": len(set(record.get("ProjectNumber") for record in clean_data_array if record.get("ProjectNumber"))),
        "total_distinct_region_names": len(set(record.get("RegionName") for record in clean_data_array if record.get("RegionName") and record.get("RegionName").strip())),
        "total_distinct_work_order_statuses": len(set(record.get("WorkOrderStatusDescription") for record in clean_data_array if record.get("WorkOrderStatusDescription") and record.get("WorkOrderStatusDescription").strip())),
        "total_distinct_crews": len(set(record.get("Crew") for record in clean_data_array if record.get("Crew") and record.get("Crew").strip())),
        "total_distinct_is_redig": len(set(record.get("IsRedig") for record in clean_data_array if record.get("IsRedig"))),
        "total_distinct_created_on_dates": len(set(record.get("CreatedOnDate") for record in clean_data_array if record.get("CreatedOnDate"))),
        "total_distinct_contractor_names": len(set(record.get("ContractorName") for record in clean_data_array if record.get("ContractorName") and record.get("ContractorName").strip())),
        "total_distinct_contractor_cwi_names": len(set(record.get("ContractorCWIName") for record in clean_data_array if record.get("ContractorCWIName") and record.get("ContractorCWIName").strip())),
        "total_distinct_contractor_nde_names": len(set(record.get("ContractorNDEName") for record in clean_data_array if record.get("ContractorNDEName") and record.get("ContractorNDEName").strip())),
        "total_distinct_contractor_cri_names": len(set(record.get("ContractorCRIName") for record in clean_data_array if record.get("ContractorCRIName") and record.get("ContractorCRIName").strip())),
        "total_distinct_managers": len(set(record.get("Manager") for record in clean_data_array if record.get("Manager") and record.get("Manager").strip())),
        "total_distinct_supervisors": len(set(record.get(f"Supervisor{i}") for record in clean_data_array for i in range(1, 5) if record.get(f"Supervisor{i}") and record.get(f"Supervisor{i}").strip())),
        "total_distinct_engineers": len(set(record.get(f"Engineer{i}") for record in clean_data_array for i in range(1, 5) if record.get(f"Engineer{i}") and record.get(f"Engineer{i}").strip())),
        "total_distinct_records_support": len(set(record.get("RecordsSupport") for record in clean_data_array if record.get("RecordsSupport") and record.get("RecordsSupport").strip()))
    }

    return analysis_results
