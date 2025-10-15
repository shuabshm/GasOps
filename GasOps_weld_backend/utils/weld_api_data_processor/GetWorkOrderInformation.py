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
            # Core Distributions
            "status_distribution": defaultdict(int),
            "region_distribution": defaultdict(int),
            "project_distribution": defaultdict(int),
            "contractor_distribution": defaultdict(int),
            
            # Personnel Distributions (Consolidated & Single)
            "engineer_distribution": defaultdict(int),     # Consolidated Engineer1-4
            "supervisor_distribution": defaultdict(int),   # Consolidated Supervisor1-4 (NOTE: Input payload shows 'SupervisorName')
            "manager_distribution": defaultdict(int),      # Consolidated Manager1-4 (NOTE: Input payload shows 'ManagerName')
            "employee_distribution": defaultdict(int),     # <-- NEW: Explicit EmployeeName distribution
            "records_support_distribution": defaultdict(int),# <-- NEW: Explicit RecordsSupport distribution

            # Specialized/CWI Personnel
            "contractor_cwi_distribution": defaultdict(int),
            "contractor_nde_distribution": defaultdict(int),
            "contractor_cri_distribution": defaultdict(int),
            "crew_distribution": defaultdict(int),
            
            # Temporal
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
        # Core Distributions
        counts["status_distribution"][record.get("WorkOrderStatusDescription", "N/A")] += 1
        counts["region_distribution"][record.get("RegionName", "N/A")] += 1
        counts["project_distribution"][record.get("ProjectNumber", "N/A")] += 1
        counts["contractor_distribution"][record.get("ContractorName", "N/A")] += 1
        counts["crew_distribution"][record.get("Crew", "N/A")] += 1
        
        # Specialized/CWI Contractor Personnel
        counts["contractor_cwi_distribution"][record.get("ContractorCWIName", "N/A")] += 1
        counts["contractor_nde_distribution"][record.get("ContractorNDEName", "N/A")] += 1
        counts["contractor_cri_distribution"][record.get("ContractorCRIName", "N/A")] += 1
        
        # Explicit Single Personnel Fields (EmployeeName, RecordsSupport)
        counts["employee_distribution"][record.get("EmployeeName", "N/A")] += 1
        counts["records_support_distribution"][record.get("RecordsSupport", "N/A")] += 1

        # Consolidated Personnel (Engineers, Supervisors, Managers)
        # Check for multi-field (Engineer1-4) or fall back to single field (EngineerName)
        
        # Engineer: Try Engineer1-4, then fall back to single 'EngineerName' if needed
        if not process_personnel(record, "Engineer", counts["engineer_distribution"]):
            single_engineer = record.get("EngineerName")
            if single_engineer and single_engineer.strip() != "":
                 counts["engineer_distribution"][single_engineer] += 1

        # Supervisor: Try Supervisor1-4, then fall back to single 'SupervisorName'
        if not process_personnel(record, "Supervisor", counts["supervisor_distribution"]):
            single_supervisor = record.get("SupervisorName")
            if single_supervisor and single_supervisor.strip() != "":
                 counts["supervisor_distribution"][single_supervisor] += 1

        # Manager: Try Manager1-4, then fall back to single 'ManagerName'
        if not process_personnel(record, "Manager", counts["manager_distribution"]):
            single_manager = record.get("ManagerName")
            if single_manager and single_manager.strip() != "":
                 counts["manager_distribution"][single_manager] += 1
        
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
    
    return analysis_results
