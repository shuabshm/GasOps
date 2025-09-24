## All available tools for WeldInsights
# Tool Functions - One for each API

from tools.execute_api import execute_api

def GetWorkOrderInformation(WorkOrderNumber=None,
                           WorkOrderStatusDescription=None,
                           ProjectNumber=None,
                           Region=None,
                           Crew=None,
                           ContractorName=None,
                           SupervisorName=None,
                           EngineerName=None,
                           IsRedig=None,
                           ContractorCWIName=None,
                           ContractorNDEName=None,
                           ContractorCRIName=None,
                           CreatedOnDate=None,
                           auth_token=None,
                           api_path="AITransmissionWorkOrder"):
    """Tool function to get work order information using various search criteria"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WorkOrderStatusDescription": WorkOrderStatusDescription,
        "ProjectNumber": ProjectNumber,
        "Region": Region,
        "Crew": Crew,
        "ContractorName": ContractorName,
        "SupervisorName": SupervisorName,
        "EngineerName": EngineerName,
        "IsRedig": IsRedig,
        "ContractorCWIName": ContractorCWIName,
        "ContractorNDEName": ContractorNDEName,
        "ContractorCRIName": ContractorCRIName,
        "CreatedOnDate": CreatedOnDate
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderInformation", parameters, auth_token, method="POST")

# Define all tools for OpenAI
def get_weldinsights_tools():
    """Define all available tools for weld insights"""
    return[
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderInformation",
                "description": "Search and retrieve work order information using various criteria including work order number, project number, region, supervisor, contractor, and engineer details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "WorkOrderStatusDescription": {
                            "type": "string",
                            "enum": ["In Progress", "Completed", "Open"],
                            "description": "Current status of the work order. Allowed values: Can be either In Progress, Completed & Open"
                        },
                        "ProjectNumber": {
                            "type": "string",
                            "description": "Project number"
                        },
                        "Region": {
                            "type": "string",
                            "enum":["Bronx", "Queens", "Westchester", ""],
                            "description": "Geographic region"
                        },
                        "Crew": {
                            "type": "string",
                            "enum": ["Company", "Contractor"],
                            "description": "Company or Contractor"
                        },
                        "ContractorName": {
                            "type": "string",
                            "description": "Name of contractor"
                        },
                        "SupervisorName": {
                            "type": "string",
                            "description": "Name of supervisor"
                        },
                        "EngineerName": {
                            "type": "string",
                            "description": "Assigned engineer name"
                        },
                        "IsRedig": {
                            "type": "boolean",
                            "description": "Indicates if the work order is a re-dig operation. True = re-dig = Maintenance Work, False = not re-dig = Construction Work"
                        },
                        "ContractorCWIName": {
                            "type": "string",
                            "description": "Name of contractor CWI"
                        },
                        "ContractorNDEName": {
                            "type": "string",
                            "description": "Name of contractor NDE"
                        },
                        "ContractorCRIName": {
                            "type": "string",
                            "description": "Assigned contractor CRI"
                        },
                        "CreatedOnDate": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Timestamp when the work order was created, in ISO 8601 format (e.g., 2025-09-22T18:50:35.105Z)."
                        },
                    },
                    "required": []
                }
            }
        }
    ]