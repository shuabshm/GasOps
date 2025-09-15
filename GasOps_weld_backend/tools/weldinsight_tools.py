# WeldInsight Tools - Welding Operations API Functions
# Individual tool functions for OpenAI function calling integration
# Handles parameter mapping and API communication for welding-related operations
#
# This module provides comprehensive access to welding data through standardized API functions.
# Functions are organized by data type and scope:
#
# Primary APIs (Entry Points):
#   - GetWorkOrderInformationAndAssignment: Search and retrieve work orders
#   - GetAllWeldDetailsByWorkOrder: Get all welds for a work order
#
# Secondary APIs (Detailed Information):
#   - GetWeldDetailsByWeldSerialNumber: Complete weld data
#   - GetMaterialAssetsByWeldSerialNumber: Material and heat information
#   - GetJoinersByWeldSerialNumber: Welder details
#   - GetVisualInspectionResultsByWeldSerialNumber: Quality control data
#
# Tertiary APIs (Advanced Inspection):
#   - GetNDEAndCRIInspectionDetails: NDE and CRI inspection data
#   - GetNDECRIAndTertiaryInspectionDetails: Complete inspection hierarchy
#
# Typical workflow:
#   1. Use GetWorkOrderInformationAndAssignment to find work orders
#   2. Use GetAllWeldDetailsByWorkOrder to get weld listings
#   3. Use specific weld serial number functions for detailed analysis
#   4. Use inspection functions for quality assurance data

from tools.calling_api_weld import call_weld_api

def GetAllWeldDetailsByWorkOrder(wr_number=None, weld_id=None, heat1=None, heat2=None, is_production=None, is_repaired=None, is_cut_out=None, auth_token=None):
    """
    Get all weld details for a work order with optional filtering parameters.
    
    Args:
        wr_number (str): Work order number (required)
        weld_id (str, optional): Specific weld ID to filter results
        heat1 (str, optional): Heat number for first material
        heat2 (str, optional): Heat number for second material  
        is_production (bool, optional): Filter for production welds
        is_repaired (bool, optional): Filter for repaired welds
        is_cut_out (bool, optional): Filter for cut-out welds
        
    Returns:
        dict: Weld details including joint numbers, completion status, materials, and inspection results
    """
    parameters = {
        "WRNumber": wr_number,
        "WeldID": weld_id,
        "Heat1": heat1,
        "Heat2": heat2,
        "IsProduction": is_production,
        "IsRepaired": is_repaired,
        "IsCutOut": is_cut_out
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetAllWeldDetailsByWorkOrder", parameters, auth_token)

def GetWorkOrderInformationAndAssignment(wr_number=None, project_number=None, region=None, contractor_type=None, contractor_name=None, engineer_name=None, is_redig=None, auth_token=None):
    """
    Get work order information and assignment details based on various search criteria.
    
    Args:
        wr_number (str, optional): Work order number
        project_number (str, optional): Project identification number
        region (str, optional): Geographic region
        contractor_type (str, optional): Type of contractor
        contractor_name (str, optional): Name of contractor
        engineer_name (str, optional): Assigned engineer name
        is_redig (bool, optional): Whether this is a re-dig operation
        
    Returns:
        dict: Work order details including status, assignments, location, dates, and contractor information
    """
    parameters = {
        "WRNumber": wr_number,
        "ProjectNumber": project_number,
        "Region": region,
        "ContractorType": contractor_type,
        "ContractorName": contractor_name,
        "EngineerName": engineer_name,
        "IsRedig": is_redig
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetWorkOrderInformationAndAssignment", parameters, auth_token)

def GetWeldDetailsByWeldSerialNumber(weld_serial_number=None, auth_token=None):
    """
    Get comprehensive weld details for a specific weld serial number.
    
    Args:
        weld_serial_number (str): Weld serial number identifier (required)
        
    Returns:
        dict: Complete weld information including joint details, materials, welders, 
              inspection results, NDT data, GPS coordinates, and equipment specifications
    """
    parameters = {"WeldSerialNumber": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetWeldDetailsByWeldSerialNumber", parameters, auth_token)

def GetMaterialAssetsByWeldSerialNumber(weld_serial_number=None, auth_token=None):
    """
    Get material assets and heat information for a specific weld.
    
    Args:
        weld_serial_number (str): Weld serial number identifier (required)
        
    Returns:
        dict: Material details including heat serials, asset types, attributes, 
              manufacturers, and MTR file IDs for both materials in the weld
    """
    parameters = {"WeldSerialNumber": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetMaterialAssetsByWeldSerialNumber", parameters, auth_token)

def GetJoinersByWeldSerialNumber(weld_serial_number=None, auth_token=None):
    """
    Get welder/joiner information for a specific weld.
    
    Args:
        weld_serial_number (str): Weld serial number identifier (required)
        
    Returns:
        dict: Welder details including names, employee IDs, position assignments,
              and combined welder information for the weld operation
    """
    parameters = {"WeldSerialNumber": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetJoinersByWeldSerialNumber", parameters, auth_token)

def GetVisualInspectionResultsByWeldSerialNumber(weld_serial_number=None, auth_token=None):
    """
    Get visual inspection results and quality control data for a specific weld.
    
    Args:
        weld_serial_number (str): Weld serial number identifier (required)
        
    Returns:
        dict: Visual inspection details including alignment, gap, access, 
              root pass quality, miter joint information, and inspector comments
    """
    parameters = {"WeldSerialNumber": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetVisualInspectionResultsByWeldSerialNumber", parameters, auth_token)

def GetNDEAndCRIInspectionDetails(wr_number=None, weld_id=None, auth_token=None):
    """
    Get Non-Destructive Examination (NDE) and Contractor Radiographic Inspection (CRI) details.
    
    Args:
        wr_number (str): Work order number (required)
        weld_id (str): Weld serial number identifier (required)
        
    Returns:
        dict: NDE and CRI inspection data including RT report numbers, radiographic dates,
              film quality, contractor information, approval status, and completion dates
    """
    parameters = {
        "WRNumber": wr_number,
        "WeldID": weld_id
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetNDEAndCRIInspectionDetailsByWeldSerialNumberAndWRNumber", parameters, auth_token)

def GetNDECRIAndTertiaryInspectionDetails(wr_number=None, weld_id=None, auth_token=None):
    """
    Get complete inspection hierarchy including NDE, CRI, and tertiary (Level 3) inspection details.
    
    Args:
        wr_number (str): Work order number (required)
        weld_id (str): Weld serial number identifier (required)
        
    Returns:
        dict: Comprehensive inspection data including all three levels of review,
              tertiary review status, approval workflow, and complete inspection timeline
    """
    parameters = {
        "WRNumber": wr_number,
        "WeldID": weld_id
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetNDECRIAndTertiaryInspectionDetailsByWeldSerialNumberAndWRNumber", parameters, auth_token)

def get_weldinsight_tools():
    """
    Define OpenAI function calling tools for WeldInsight operations.
    
    Returns comprehensive tool definitions for welding and work order management,
    enabling AI agents to intelligently select and use appropriate functions.
    
    The tools are organized in three categories:
    
    1. Primary APIs: Entry points for work order discovery and bulk weld data
    2. Secondary APIs: Detailed information for specific welds
    3. Tertiary APIs: Advanced inspection and quality assurance data
    
    Usage Examples:
    - Find work orders by contractor: GetWorkOrderInformationAndAssignment(contractor_name="ABC Corp")
    - Get all welds for a work order: GetAllWeldDetailsByWorkOrder(wr_number="12345")
    - Get complete weld details: GetWeldDetailsByWeldSerialNumber(weld_serial_number="W001")
    - Check inspection status: GetNDEAndCRIInspectionDetails(wr_number="12345", weld_id="W001")
    
    Returns:
        list: OpenAI tool definitions for welding-related functions
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "GetAllWeldDetailsByWorkOrder",
                "description": "Get all weld details for a work order with optional filtering by weld ID, heat numbers, and status flags",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "wr_number": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "weld_id": {
                            "type": "string",
                            "description": "Specific weld ID to filter results"
                        },
                        "heat1": {
                            "type": "string",
                            "description": "Heat number for first material"
                        },
                        "heat2": {
                            "type": "string",
                            "description": "Heat number for second material"
                        },
                        "is_production": {
                            "type": "boolean",
                            "description": "Filter for production welds"
                        },
                        "is_repaired": {
                            "type": "boolean",
                            "description": "Filter for repaired welds"
                        },
                        "is_cut_out": {
                            "type": "boolean",
                            "description": "Filter for cut-out welds"
                        }
                    },
                    "required": ["wr_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderInformationAndAssignment",
                "description": "Search and retrieve work order information using various criteria including work order number, project, region, contractor, and engineer details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "wr_number": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "project_number": {
                            "type": "string",
                            "description": "Project identification number"
                        },
                        "region": {
                            "type": "string",
                            "description": "Geographic region"
                        },
                        "contractor_type": {
                            "type": "string",
                            "description": "Type of contractor"
                        },
                        "contractor_name": {
                            "type": "string",
                            "description": "Name of contractor"
                        },
                        "engineer_name": {
                            "type": "string",
                            "description": "Assigned engineer name"
                        },
                        "is_redig": {
                            "type": "boolean",
                            "description": "Whether this is a re-dig operation"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWeldDetailsByWeldSerialNumber",
                "description": "Get comprehensive weld details including joint information, materials, welders, inspection results, NDT data, and equipment specifications for a specific weld",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "weld_serial_number": {
                            "type": "string",
                            "description": "Weld serial number identifier"
                        }
                    },
                    "required": ["weld_serial_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetMaterialAssetsByWeldSerialNumber",
                "description": "Get detailed material information including heat serials, asset types, attributes, manufacturers, and MTR file IDs for both materials in a weld",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "weld_serial_number": {
                            "type": "string",
                            "description": "Weld serial number"
                        }
                    },
                    "required": ["weld_serial_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetJoinersByWeldSerialNumber",
                "description": "Get welder and joiner information including names, employee IDs, position assignments for a specific weld operation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "weld_serial_number": {
                            "type": "string",
                            "description": "Weld serial number"
                        }
                    },
                    "required": ["weld_serial_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetVisualInspectionResultsByWeldSerialNumber",
                "description": "Get visual inspection and quality control results including alignment, gap, access, root pass quality, and inspector comments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "weld_serial_number": {
                            "type": "string",
                            "description": "Weld serial number"
                        }
                    },
                    "required": ["weld_serial_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetNDEAndCRIInspectionDetails",
                "description": "Get Non-Destructive Examination and Contractor Radiographic Inspection details including RT reports, film quality, contractor information, and approval status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "wr_number": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "weld_id": {
                            "type": "string",
                            "description": "Weld identifier"
                        }
                    },
                    "required": ["wr_number", "weld_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetNDECRIAndTertiaryInspectionDetails",
                "description": "Get complete inspection hierarchy including NDE, CRI, and tertiary (Level 3) inspection details with approval workflow and timeline",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "wr_number": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "weld_id": {
                            "type": "string",
                            "description": "Weld identifier"
                        }
                    },
                    "required": ["wr_number", "weld_id"]
                }
            }
        }
    ]