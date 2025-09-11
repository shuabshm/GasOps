# WeldInsight Tools - Welding Operations API Functions
# Individual tool functions for OpenAI function calling integration
# Handles parameter mapping and API communication for welding-related operations

from tools.calling_api_weld import call_weld_api

def GetAllWeldDetailsByWorkOrder(wr_number=None):
    """Tool function to get all weld details for a work order"""
    parameters = {"wr_number": wr_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetAllWeldDetailsByWorkOrder", parameters)

def GetWorkOrderInformationAndAssignment(wr_number=None):
    """Tool function to get work order information and assignment"""
    parameters = {"wr_number": wr_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetWorkOrderInformationAndAssignment", parameters)

def GetWeldDetailsByWeldSerialNumber(weld_serial_number=None):
    """Tool function to get weld details by weld serial number"""
    parameters = {"weld_serial_number": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetWeldDetailsByWeldSerialNumber", parameters)

def GetMaterialAssetsByWeldSerialNumber(weld_serial_number=None):
    """Tool function to get material assets by weld serial number"""
    parameters = {"weld_serial_number": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetMaterialAssetsByWeldSerialNumber", parameters)

def GetJoinersByWeldSerialNumber(weld_serial_number=None):
    """Tool function to get joiners by weld serial number"""
    parameters = {"weld_serial_number": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetJoinersByWeldSerialNumber", parameters)

def GetVisualInspectionResultsByWeldSerialNumber(weld_serial_number=None):
    """Tool function to get visual inspection results by weld serial number"""
    parameters = {"weld_serial_number": weld_serial_number}
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetVisualInspectionResultsByWeldSerialNumber", parameters)

def GetNDEAndCRIInspectionDetails(wr_number=None, weld_id=None):
    """Tool function to get NDE and CRI inspection details"""
    parameters = {
        "wr_number": wr_number,
        "weld_id": weld_id
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetNDEAndCRIInspectionDetailsByWeldSerialNumberAndWRNumber", parameters)

def GetNDECRIAndTertiaryInspectionDetails(wr_number=None, weld_id=None):
    """Tool function to get NDE, CRI and tertiary inspection details"""
    parameters = {
        "wr_number": wr_number,
        "weld_id": weld_id
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return call_weld_api("GetNDECRIAndTertiaryInspectionDetailsByWeldSerialNumberAndWRNumber", parameters)

def get_weldinsight_tools():
    """
    Define OpenAI function calling tools for WeldInsight operations.
    
    Returns comprehensive tool definitions for welding and work order management,
    enabling AI agents to intelligently select and use appropriate functions.
    
    Returns:
        list: OpenAI tool definitions for welding-related functions
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "GetAllWeldDetailsByWorkOrder",
                "description": "Get all weld details for a specific work order number",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "wr_number": {
                            "type": "string",
                            "description": "Work order number"
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
                "description": "Get work order information and assignment details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "wr_number": {
                            "type": "string",
                            "description": "Work order number"
                        }
                    },
                    "required": ["wr_number"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWeldDetailsByWeldSerialNumber",
                "description": "Get specific weld details by weld serial number",
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
                "description": "Get material assets associated with a specific weld",
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
                "description": "Get joiner information for a specific weld",
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
                "description": "Get visual inspection results for a specific weld",
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
                "description": "Get NDE (Non-Destructive Examination) and CRI inspection details",
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
                "description": "Get NDE, CRI and tertiary inspection details",
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