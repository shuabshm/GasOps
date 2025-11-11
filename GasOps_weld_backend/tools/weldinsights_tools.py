## All available tools for WeldInsights
# Tool Functions - One for each API

from tools.execute_api import execute_api

def GetWorkOrderInformation(WorkOrderNumber=None,
                           WorkOrderStatusDescription=None,
                           ProjectNumber=None,
                           Region=None,
                           Crew=None,
                           ContractorName=None,
                           ContractorCWIName=None,
                           ContractorNDEName=None,
                           ContractorCRIName=None,
                           EmployeeName=None,
                           ManagerName=None,
                           SupervisorName=None,
                           EngineerName=None,
                           RecordsSupportName=None,
                           IsRedig=None,
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
        "ContractorCWIName": ContractorCWIName,
        "ContractorNDEName": ContractorNDEName,
        "ContractorCRIName": ContractorCRIName,
        "EmployeeName": EmployeeName,
        "ManagerName": ManagerName,
        "SupervisorName": SupervisorName,
        "EngineerName": EngineerName,
        "RecordsSupportName": RecordsSupportName,
        "IsRedig": IsRedig,
        "CreatedOnDate": CreatedOnDate
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderInformation", parameters, auth_token, method="POST")


def GetWeldDetailsbyWorkOrderNumberandCriteria(WorkOrderNumber,
                                               WeldCategory=None,
                                               TieinWeld=None,
                                               Prefab=None,
                                               Gap=None,
                                               HeatSerialNumber=None,
                                               Asset=None,
                                               AssetSubcategory=None,
                                               Material=None,
                                               Size=None,
                                               Manufacturer=None,
                                               RootRodClass=None,
                                               FillerRodClass=None,
                                               HotRodClass=None,
                                               CapRodClass=None,
                                               WeldUnlocked=None,
                                               AddedtoWeldMap=None,
                                               WelderName=None,
                                               CWIName=None,
                                               CWIResult=None,
                                               NDEName=None,
                                               NDEResult=None,
                                               CRIName=None,
                                               CRIResult=None,
                                               TRName=None,
                                               TRResult=None,
                                               GroupBy=None,
                                               auth_token=None,
                                               api_path="AITransmissionWorkOrder"):
    """Tool function to get detailed weld information by work order number and various weld criteria"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldCategory": WeldCategory,
        "TieinWeld": TieinWeld,
        "Prefab": Prefab,
        "Gap": Gap,
        "HeatSerialNumber": HeatSerialNumber,
        "Asset": Asset,
        "AssetSubcategory": AssetSubcategory,
        "Material": Material,
        "Size": Size,
        "Manufacturer": Manufacturer,
        "RootRodClass": RootRodClass,
        "FillerRodClass": FillerRodClass,
        "HotRodClass": HotRodClass,
        "CapRodClass": CapRodClass,
        "WeldUnlocked": WeldUnlocked,
        "AddedtoWeldMap": AddedtoWeldMap,
        "WelderName": WelderName,
        "CWIName": CWIName,
        "CWIResult": CWIResult,
        "NDEName": NDEName,
        "NDEResult": NDEResult,
        "CRIName": CRIName,
        "CRIResult": CRIResult,
        "TRName": TRName,
        "TRResult": TRResult,
        "GroupBy": GroupBy
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWeldDetailsbyWorkOrderNumberandCriteria", parameters, auth_token, method="POST")


def GetWelderNameDetailsbyWorkOrderNumberandCriteria(WorkOrderNumber,
                                                      WeldCategory=None,
                                                      auth_token=None,
                                                      api_path="AITransmissionWorkOrder"):
    """Tool function to get welder name details and assignments for specific work orders by category"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldCategory": WeldCategory
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWelderNameDetailsbyWorkOrderNumberandCriteria", parameters, auth_token, method="POST")


def GetUnlockWeldDetailsbyWorkOrderNumberandCriteria(WorkOrderNumber,
                                                       UnlockedBy=None,
                                                       UpdatedBy=None,
                                                       UpdateCompleted=None,
                                                       auth_token=None,
                                                       api_path="AITransmissionWorkOrder"):
    """Tool function to get unlocked weld details for requested work order number and other criteria"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "UnlockedBy": UnlockedBy,
        "UpdatedBy": UpdatedBy,
        "UpdateCompleted": UpdateCompleted
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetUnlockWeldDetailsbyWorkOrderNumberandCriteria", parameters, auth_token, method="POST")


def GetWorkOrderDetailsbyCriteria(ProjectNumber=None,
                                    HeatSerialNumber=None,
                                    WeldSerialNumber=None,
                                    NDEReportNumber=None,
                                    auth_token=None,
                                    api_path="AITransmissionWorkOrder"):
    """Tool function to get work order details by Heat Number/NDE Report Number/Weld Serial Number"""

    parameters = {
        "ProjectNumber": ProjectNumber,
        "HeatSerialNumber": HeatSerialNumber,
        "WeldSerialNumber": WeldSerialNumber,
        "NDEReportNumber": NDEReportNumber
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderDetailsbyCriteria", parameters, auth_token, method="POST")


def GetNDEReportNumbersbyWorkOrderNumber(WorkOrderNumber,
                                          auth_token=None,
                                          api_path="AITransmissionWorkOrder"):
    """Tool function to get list of all NDE report numbers and their type by requested work order number"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetNDEReportNumbersbyWorkOrderNumber", parameters, auth_token, method="POST")


def GetWorkOrderNDEIndicationsbyCriteria(WorkOrderNumber=None,
                                          WeldSerialNumber=None,
                                          WelderName=None,
                                          NDEName=None,
                                          GroupBy=None,
                                          auth_token=None,
                                          api_path="AITransmissionWorkOrder"):
    """Tool function to get NDE indication details for requested work order number/weld serial number with grouping by specified fields"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldSerialNumber": WeldSerialNumber,
        "WelderName": WelderName,
        "NDEName": NDEName,
        "GroupBy": GroupBy
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderNDEIndicationsbyCriteria", parameters, auth_token, method="POST")


def GetWorkOrderRejactableNDEIndicationsbyCriteria(WorkOrderNumber=None,
                                                     WeldSerialNumber=None,
                                                     WelderName=None,
                                                     NDEName=None,
                                                     GroupBy=None,
                                                     auth_token=None,
                                                     api_path="AITransmissionWorkOrder"):
    """Tool function to get rejectable NDE indication details for requested work order number/weld serial number with grouping by specified fields"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldSerialNumber": WeldSerialNumber,
        "WelderName": WelderName,
        "NDEName": NDEName,
        "GroupBy": GroupBy
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderRejactableNDEIndicationsbyCriteria", parameters, auth_token, method="POST")


def GetReshootDetailsbyWorkOrderNumberandCriteria(WorkOrderNumber,
                                                    UpdateCompleted=None,
                                                    auth_token=None,
                                                    api_path="AITransmissionWorkOrder"):
    """Tool function to get reshoot weld details for requested work order number with filtering by update completion status"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "UpdateCompleted": UpdateCompleted
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetReshootDetailsbyWorkOrderNumberandCriteria", parameters, auth_token, method="POST")


def GetWeldsbyNDEIndicationandWorkOrderNumber(WorkOrderNumber,
                                                NDEIndication,
                                                auth_token=None,
                                                api_path="AITransmissionWorkOrder"):
    """Tool function to get welds for requested work order number filtered by specific NDE indication type"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "NDEIndication": NDEIndication
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWeldsbyNDEIndicationandWorkOrderNumber", parameters, auth_token, method="POST")


def GetWorkOrderCRIIndicationsbyCriteria(WorkOrderNumber=None,
                                          WeldSerialNumber=None,
                                          WelderName=None,
                                          CRIName=None,
                                          GroupBy=None,
                                          auth_token=None,
                                          api_path="AITransmissionWorkOrder"):
    """Tool function to get CRI indication details with grouping by specified fields"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldSerialNumber": WeldSerialNumber,
        "WelderName": WelderName,
        "CRIName": CRIName,
        "GroupBy": GroupBy
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderCRIIndicationsbyCriteria", parameters, auth_token, method="POST")


def GetWorkOrderRejactableCRIIndicationsbyCriteria(WorkOrderNumber=None,
                                                     WeldSerialNumber=None,
                                                     WelderName=None,
                                                     CRIName=None,
                                                     GroupBy=None,
                                                     auth_token=None,
                                                     api_path="AITransmissionWorkOrder"):
    """Tool function to get rejectable CRI indication details with grouping by specified fields"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldSerialNumber": WeldSerialNumber,
        "WelderName": WelderName,
        "CRIName": CRIName,
        "GroupBy": GroupBy
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderRejactableCRIIndicationsbyCriteria", parameters, auth_token, method="POST")


def GetWorkOrderTRIndicationsbyCriteria(WorkOrderNumber=None,
                                        WeldSerialNumber=None,
                                        WelderName=None,
                                        TRName=None,
                                        GroupBy=None,
                                        auth_token=None,
                                        api_path="AITransmissionWorkOrder"):
    """Tool function to get TR indication details with grouping by specified fields"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldSerialNumber": WeldSerialNumber,
        "WelderName": WelderName,
        "TRName": TRName,
        "GroupBy": GroupBy
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderTRIndicationsbyCriteria", parameters, auth_token, method="POST")


def GetWorkOrderRejactableTRIndicationsbyCriteria(WorkOrderNumber=None,
                                                   WeldSerialNumber=None,
                                                   WelderName=None,
                                                   TRName=None,
                                                   GroupBy=None,
                                                   auth_token=None,
                                                   api_path="AITransmissionWorkOrder"):
    """Tool function to get rejectable TR indication details for requested work order number/weld serial number with grouping by specified fields"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "WeldSerialNumber": WeldSerialNumber,
        "WelderName": WelderName,
        "TRName": TRName,
        "GroupBy": GroupBy
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrderRejactableTRIndicationsbyCriteria", parameters, auth_token, method="POST")


def GetWeldsbyCRIIndicationandWorkOrderNumber(WorkOrderNumber,
                                                CRIIndication,
                                                auth_token=None,
                                                api_path="AITransmissionWorkOrder"):
    """Tool function to get welds for requested work order number filtered by specific CRI indication type"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "CRIIndication": CRIIndication
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWeldsbyCRIIndicationandWorkOrderNumber", parameters, auth_token, method="POST")


def GetWeldsbyTRIndicationandWorkOrderNumber(WorkOrderNumber,
                                              TRIndication,
                                              auth_token=None,
                                              api_path="AITransmissionWorkOrder"):
    """Tool function to get welds for requested work order number filtered by specific TR indication type"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "TRIndication": TRIndication
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWeldsbyTRIndicationandWorkOrderNumber", parameters, auth_token, method="POST")


def GetNDEReportProcessingDetailsbyWeldSerialNumber(WeldSerialNumber,
                                                      auth_token=None,
                                                      api_path="AITransmissionWorkOrder"):
    """Tool function to get list of all NDE report numbers and their type by requested weld serial number"""

    parameters = {
        "WeldSerialNumber": WeldSerialNumber
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetNDEReportProcessingDetailsbyWeldSerialNumber", parameters, auth_token, method="POST")


def GetDetailsbyWeldSerialNumber(WeldSerialNumber,
                                   ProjectNumber=None,
                                   HeatSerialNumber=None,
                                   NDEReportNumber=None,
                                   auth_token=None,
                                   api_path="AITransmissionWorkOrder"):
    """Tool function to get comprehensive weld details by weld serial number with optional filters"""

    parameters = {
        "WeldSerialNumber": WeldSerialNumber,
        "ProjectNumber": ProjectNumber,
        "HeatSerialNumber": HeatSerialNumber,
        "NDEReportNumber": NDEReportNumber
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetDetailsbyWeldSerialNumber", parameters, auth_token, method="POST")


def GetHeatNumberDetailsbyWorkOrderNumberandCriteria(WorkOrderNumber,
                                                       Asset=None,
                                                       AssetSubcategory=None,
                                                       Material=None,
                                                       Size=None,
                                                       Manufacturer=None,
                                                       auth_token=None,
                                                       api_path="AITransmissionWorkOrder"):
    """Tool function to get heat number details for requested work order number with optional filtering criteria"""

    parameters = {
        "WorkOrderNumber": WorkOrderNumber,
        "Asset": Asset,
        "AssetSubcategory": AssetSubcategory,
        "Material": Material,
        "Size": Size,
        "Manufacturer": Manufacturer
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetHeatNumberDetailsbyWorkOrderNumberandCriteria", parameters, auth_token, method="POST")


def GetWorkOrdersbyWelderName(WelderName,
                                auth_token=None,
                                api_path="AITransmissionWorkOrder"):
    """Tool function to get list of work orders where there are welds made by respective welder name"""

    parameters = {
        "WelderName": WelderName
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}
    return execute_api(api_path, "GetWorkOrdersbyWelderName", parameters, auth_token, method="POST")


def GetWorkOrderSummary(WorkOrderNumber,
                        auth_token=None,
                        api_path="AITransmissionWorkOrder"):
    """
    Tool function to get comprehensive work order summary using existing transformers.

    This approach:
    1. Calls 8 different APIs to get all work order data
    2. Uses existing API-specific transformers to process each API's data
    3. Combines all pre-processed data and makes ONE AI call for final synthesis
    4. Returns a cohesive, well-structured comprehensive work order summary

    Benefits:
    - Reuses existing API-specific prompts and transformers (DRY principle)
    - Makes only ONE AI call instead of 9 (more efficient)
    - 100% data coverage (uses existing analyzers that extract all fields)
    - Token-efficient (AI sees pre-processed data, not massive raw data)
    - Scalable to any work order size
    - Maintainable (no duplicate prompt logic)
    """
    import logging
    from config.azure_client import get_azure_chat_openai
    from utils.data_extractor import extract_clean_data
    from utils.data_transformers import get_transformer
    from prompts.weld_apis_prompts.GetWorkOrderSummary import get_api_prompt

    logger = logging.getLogger(__name__)

    # Initialize Azure OpenAI client for AI calls
    try:
        azure_client, azureopenai = get_azure_chat_openai()
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
        return {
            "success": False,
            "error": f"AI client initialization failed: {str(e)}",
            "status_code": 500
        }

    logger.info(f"Starting work order summary for WorkOrderNumber: {WorkOrderNumber}")

    # Define all APIs to call in sequence
    apis_to_call = [
        {
            "name": "GetWorkOrderInformation",
            "function": GetWorkOrderInformation,
            "params": {"WorkOrderNumber": WorkOrderNumber},
            "section_title": "Work Order Information"
        },
        {
            "name": "GetWeldDetailsbyWorkOrderNumberandCriteria",
            "function": GetWeldDetailsbyWorkOrderNumberandCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber},
            "section_title": "Weld Details & Inspection Results"
        },
        {
            "name": "GetWelderNameDetailsbyWorkOrderNumberandCriteria",
            "function": GetWelderNameDetailsbyWorkOrderNumberandCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber},
            "section_title": "Welder Performance"
        },
        {
            "name": "GetWorkOrderNDEIndicationsbyCriteria",
            "function": GetWorkOrderNDEIndicationsbyCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber, "GroupBy": ["WorkOrderNumber"]},
            "section_title": "NDE Indications"
        },
        {
            "name": "GetWorkOrderRejactableNDEIndicationsbyCriteria",
            "function": GetWorkOrderRejactableNDEIndicationsbyCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber, "GroupBy": ["WorkOrderNumber"]},
            "section_title": "Rejectable NDE Indications"
        },
        {
            "name": "GetWorkOrderCRIIndicationsbyCriteria",
            "function": GetWorkOrderCRIIndicationsbyCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber, "GroupBy": ["WorkOrderNumber"]},
            "section_title": "CRI Indications"
        },
        {
            "name": "GetWorkOrderRejactableCRIIndicationsbyCriteria",
            "function": GetWorkOrderRejactableCRIIndicationsbyCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber, "GroupBy": ["WorkOrderNumber"]},
            "section_title": "Rejectable CRI Indications"
        },
        {
            "name": "GetWorkOrderTRIndicationsbyCriteria",
            "function": GetWorkOrderTRIndicationsbyCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber, "GroupBy": ["WorkOrderNumber"]},
            "section_title": "TR Indications"
        },
        {
            "name": "GetWorkOrderRejactableTRIndicationsbyCriteria",
            "function": GetWorkOrderRejactableTRIndicationsbyCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber, "GroupBy": ["WorkOrderNumber"]},
            "section_title": "Rejectable TR Indications"
        },
        {
            "name": "GetReshootDetailsbyWorkOrderNumberandCriteria",
            "function": GetReshootDetailsbyWorkOrderNumberandCriteria,
            "params": {"WorkOrderNumber": WorkOrderNumber},
            "section_title": "Reshoot Details"
        }
    ]

    processed_apis = []

    try:
        # Step 1: Call all APIs and process with their existing transformers
        for i, api_config in enumerate(apis_to_call, 1):
            api_name = api_config["name"]
            api_function = api_config["function"]
            api_params = api_config["params"]
            section_title = api_config["section_title"]

            logger.info(f"[{i}/8] Processing {api_name}...")

            # Call the API
            try:
                api_result = api_function(**api_params, auth_token=auth_token, api_path=api_path)

                if not api_result.get("success"):
                    logger.warning(f"[{i}/8] {api_name} returned no data or error")
                    processed_apis.append({
                        "section_title": section_title,
                        "api_name": api_name,
                        "analysis_results": {},
                        "total_records": 0
                    })
                    continue

                # Extract clean data
                clean_data = extract_clean_data([{
                    "api_name": api_name,
                    "parameters": api_params,
                    "data": api_result
                }])

                if not clean_data or len(clean_data) == 0:
                    logger.warning(f"[{i}/8] {api_name} returned empty data")
                    processed_apis.append({
                        "section_title": section_title,
                        "api_name": api_name,
                        "analysis_results": {},
                        "total_records": 0
                    })
                    continue

                # Use existing transformer to process data
                transformer = get_transformer(api_name)
                if transformer:
                    analyzed_data = transformer(clean_data, api_params)
                else:
                    analyzed_data = {
                        "total_records": len(clean_data),
                        "raw_data": clean_data,
                        "filter_applied": api_params
                    }

                total_records = analyzed_data.get("total_records", 0)
                logger.info(f"[{i}/8] {api_name} processed: {total_records} records")

                processed_apis.append({
                    "section_title": section_title,
                    "api_name": api_name,
                    "analysis_results": analyzed_data,
                    "total_records": total_records
                })

            except Exception as e:
                logger.error(f"[{i}/8] Error processing {api_name}: {str(e)}", exc_info=True)
                processed_apis.append({
                    "section_title": section_title,
                    "api_name": api_name,
                    "analysis_results": {"error": str(e)},
                    "total_records": 0
                })

        # Log API execution summary
        logger.info("=" * 80)
        logger.info("API EXECUTION SUMMARY")
        logger.info("=" * 80)

        successful_apis = []
        failed_apis = []
        no_data_apis = []

        for api_data in processed_apis:
            api_name = api_data["api_name"]
            total_records = api_data["total_records"]
            has_error = "error" in api_data["analysis_results"]

            if has_error:
                failed_apis.append(api_name)
            elif total_records == 0:
                no_data_apis.append(api_name)
            else:
                successful_apis.append(api_name)

        logger.info(f"[SUCCESS] Successfully executed: {len(successful_apis)}/{len(processed_apis)} APIs")
        for api in successful_apis:
            logger.info(f"  [OK] {api}")

        if no_data_apis:
            logger.info(f"[WARNING] No data returned: {len(no_data_apis)} APIs")
            for api in no_data_apis:
                logger.info(f"  [NO DATA] {api}")

        if failed_apis:
            logger.info(f"[FAILED] Failed: {len(failed_apis)} APIs")
            for api in failed_apis:
                logger.info(f"  [ERROR] {api}")

        logger.info("=" * 80)

        # Step 2: Generate comprehensive summary with ONE AI call
        logger.info("Generating comprehensive summary from pre-processed data...")

        # Use the existing prompt that knows how to handle pre-processed data
        summary_prompt = get_api_prompt(WorkOrderNumber, processed_apis)

        # Single AI call for final synthesis
        final_response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.2
        )

        final_summary = final_response.choices[0].message.content
        logger.info("Comprehensive summary generated successfully")

        # Return in standard API response format
        return {
            "success": True,
            "data": {
                "Data": {
                    "WorkOrderNumber": WorkOrderNumber,
                    "ComprehensiveSummary": final_summary,
                    "ExecutionSummary": {
                        "total_apis": len(processed_apis),
                        "successful": len(successful_apis),
                        "no_data": len(no_data_apis),
                        "failed": len(failed_apis),
                        "successful_apis": successful_apis,
                        "no_data_apis": no_data_apis,
                        "failed_apis": failed_apis
                    }
                }
            },
            "status_code": 200
        }

    except Exception as e:
        logger.error(f"Error in GetWorkOrderSummary: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "status_code": 500
        }


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
                            "description": "Name of the contractor('Bond', 'CAC', 'MFM', 'Network', 'Danella',etc.)"
                        },
                        "SupervisorName": {
                            "type": "string",
                            "description": "supervisor name assigned to the work order"
                        },
                        "EngineerName": {
                            "type": "string",
                            "description": "Engineer name assigned to the work order"
                        },
                        "EmployeeName": {
                            "type": "string",
                            "description": "Name of any employee associated with the work order (Engineer, Supervisor, Records Support, etc.)"
                        },
                        "ManagerName": {
                            "type": "string",
                            "description": "Manager name Assigned to Manager"
                        },
                        "RecordsSupportName": {
                            "type": "string",
                            "description": "Name of records support assigned to the work order"
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
                            "description": "Assigned contractor CRI/L2/L3 Peer review or reviewer name"
                        },
                        "CreatedOnDate": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Timestamp when the work order was created in YYYY-MM-DDTHH:MM:SS.SSSZ format (e.g., 2025-09-22T18:50:35.105Z)."
                        },
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWeldDetailsbyWorkOrderNumberandCriteria",
                "description": "Get detailed weld information for a specific work order with various filtering criteria including weld category, inspection results, welders, and material details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "WeldCategory": {
                            "type": "string",
                            "enum": ["Production", "Repaired", "CutOut"],
                            "description": "Category of weld work. Allowed values: Production, Repaired, CutOut"
                        },
                        "TieinWeld": {
                            "type": "string",
                            "enum": ["Yes", "No"],
                            "description": "Whether this is a tie-in weld. Allowed values: Yes, No"
                        },
                        "Prefab": {
                            "type": "string",
                            "enum": ["Yes", "No"],
                            "description": "Whether this weld involves prefabricated components. Allowed values: Yes, No"
                        },
                        "Gap": {
                            "type": "string",
                            "enum": ["Yes", "No"],
                            "description": "Whether a gap was noted during welding. Allowed values: Yes, No"
                        },
                        "HeatSerialNumber": {
                            "type": "string",
                            "description": "Heat serial number for material traceability"
                        },
                        "Asset": {
                            "type": "string",
                            "description": "Asset identifier"
                        },
                        "AssetSubcategory": {
                            "type": "string",
                            "description": "Asset subcategory classification"
                        },
                        "Material": {
                            "type": "string",
                            "description": "Material type or specification"
                        },
                        "Size": {
                            "type": "string",
                            "description": "Size specification of the weld component"
                        },
                        "Manufacturer": {
                            "type": "string",
                            "description": "Manufacturer of the weld components"
                        },
                        "RootRodClass": {
                            "type": "string",
                            "description": "Classification of root welding rod used"
                        },
                        "FillerRodClass": {
                            "type": "string",
                            "description": "Classification of filler welding rod used"
                        },
                        "HotRodClass": {
                            "type": "string",
                            "description": "Classification of hot pass welding rod used"
                        },
                        "CapRodClass": {
                            "type": "string",
                            "description": "Classification of cap pass welding rod used"
                        },
                        "WeldUnlocked": {
                            "type": "string",
                            "enum": ["Yes", "No"],
                            "description": "Whether the weld is unlocked for editing. Allowed values: Yes, No"
                        },
                        "AddedtoWeldMap": {
                            "type": "string",
                            "enum": ["Yes", "No"],
                            "description": "Whether weld has been added to the weld map. Allowed values: Yes, No"
                        },
                        "WelderName": {
                            "type": "string",
                            "description": "Name of the welder who performed the weld"
                        },
                        "CWIName": {
                            "type": "string",
                            "description": "Name of the Certified Welding Inspector (CWI)"
                        },
                        "CWIResult": {
                            "type": "string",
                            "enum": ["Accept", "Reject", "Pending"],
                            "description": "Result of CWI inspection. Allowed values: Accept, Reject, Pending"
                        },
                        "NDEName": {
                            "type": "string",
                            "description": "Name of the Non-Destructive Examination (NDE) inspector"
                        },
                        "NDEResult": {
                            "type": "string",
                            "enum": ["Accept", "Reject", "In Process", "Pending"],
                            "description": "Result of NDE inspection. Allowed values: Accept, Reject, In Process, Pending"
                        },
                        "CRIName": {
                            "type": "string",
                            "description": "Name of the Construction Records Inspector (CRI)"
                        },
                        "CRIResult": {
                            "type": "string",
                            "enum": ["Accept", "Reject", "In Process", "Pending"],
                            "description": "Result of CRI inspection. Allowed values: Accept, Reject, In Process, Pending"
                        },
                        "TRName": {
                            "type": "string",
                            "description": "Name of the Technical Reviewer (TR)"
                        },
                        "TRResult": {
                            "type": "string",
                            "enum": ["Approved", "Rejected", "Pending"],
                            "description": "Result of TR review. Allowed values: Approved, Rejected, Pending"
                        },
                        "GroupBy": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Fields to group results by (e.g., WelderName, WeldSerialNumber, CWIResult, etc.)"
                        }
                    },
                    "required": ["WorkOrderNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWelderNameDetailsbyWorkOrderNumberandCriteria",
                "description": "Get welder name details and assignments for specific work orders by category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "WeldCategory": {
                            "type": "string",
                            "enum": ["Production", "Repaired", "CutOut"],
                            "description": "Category of weld work. Allowed values: Production, Repaired, CutOut"
                        }
                    },
                    "required": ["WorkOrderNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetUnlockWeldDetailsbyWorkOrderNumberandCriteria",
                "description": "Get unlocked weld details for requested work order number and other criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "UnlockedBy": {
                            "type": "string",
                            "description": "Name of the user who unlocked the weld"
                        },
                        "UpdatedBy": {
                            "type": "string",
                            "description": "Name of the user who updated the weld after unlocking"
                        },
                        "UpdateCompleted": {
                            "type": "string",
                            "enum": ["Yes", "No"],
                            "description": "Whether the update has been completed. Allowed values: Yes, No."
                        }
                    },
                    "required": ["WorkOrderNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderDetailsbyCriteria",
                "description": "Get work order details by searching with project number, heat serial number, weld serial number, or NDE report number. At least one search parameter must be provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ProjectNumber": {
                            "type": "string",
                            "description": "Project number to search for"
                        },
                        "HeatSerialNumber": {
                            "type": "string",
                            "description": "Heat serial number to search for"
                        },
                        "WeldSerialNumber": {
                            "type": "string",
                            "description": "Weld serial number to search for"
                        },
                        "NDEReportNumber": {
                            "type": "string",
                            "description": "NDE report number to search for"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetNDEReportNumbersbyWorkOrderNumber",
                "description": "Get list of all NDE report numbers and their type by requested work order number",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        }
                    },
                    "required": ["WorkOrderNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderNDEIndicationsbyCriteria",
                "description": "Get NDE indication details for requested work order number/weld serial number with grouping by specified fields. At least one of WorkOrderNumber or WeldSerialNumber must be provided, and GroupBy is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "WeldSerialNumber": {
                            "type": "string",
                            "description": "Weld serial number"
                        },
                        "WelderName": {
                            "type": "string",
                            "description": "Welder name for filtering"
                        },
                        "NDEName": {
                            "type": "string",
                            "description": "NDE inspector name for filtering"
                        },
                        "GroupBy": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Fields to group results by (e.g., WorkOrderNumber, WeldSerialNumber, NDEName, WelderName). This parameter is required."
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderRejactableNDEIndicationsbyCriteria",
                "description": "Get rejectable NDE indication details for requested work order number/weld serial number with grouping by specified fields. At least one of WorkOrderNumber or WeldSerialNumber must be provided, and GroupBy is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "WeldSerialNumber": {
                            "type": "string",
                            "description": "Weld serial number"
                        },
                        "WelderName": {
                            "type": "string",
                            "description": "Welder name for filtering"
                        },
                        "NDEName": {
                            "type": "string",
                            "description": "NDE inspector name for filtering"
                        },
                        "GroupBy": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Fields to group results by (e.g., WorkOrderNumber, WeldSerialNumber, Indication, NDEName, WelderName). This parameter is required."
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderTRIndicationsbyCriteria",
                "description": "Get TR (Test Results) indication details for requested work order number/weld serial number with grouping by specified fields. At least one of WorkOrderNumber or WeldSerialNumber must be provided, and GroupBy is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "WeldSerialNumber": {
                            "type": "string",
                            "description": "Weld serial number"
                        },
                        "WelderName": {
                            "type": "string",
                            "description": "Welder name for filtering"
                        },
                        "TRName": {
                            "type": "string",
                            "description": "TR inspector name for filtering"
                        },
                        "GroupBy": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Fields to group results by (e.g., WorkOrderNumber, WeldSerialNumber, Indication, TRName, WelderName). This parameter is required."
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderRejactableTRIndicationsbyCriteria",
                "description": "Get rejectable TR (Tertiary Review) indication details for requested work order number/weld serial number with grouping by specified fields. At least one of WorkOrderNumber or WeldSerialNumber must be provided, and GroupBy is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number"
                        },
                        "WeldSerialNumber": {
                            "type": "string",
                            "description": "Weld serial number"
                        },
                        "WelderName": {
                            "type": "string",
                            "description": "Welder name for filtering"
                        },
                        "TRName": {
                            "type": "string",
                            "description": "TR inspector name for filtering"
                        },
                        "GroupBy": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Fields to group results by (e.g., WorkOrderNumber, WeldSerialNumber, Indication, TRName, WelderName). This parameter is required."
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetReshootDetailsbyWorkOrderNumberandCriteria",
                "description": "Get reshoot weld details for requested work order number with filtering by update completion status. WorkOrderNumber is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "UpdateCompleted": {
                            "type": "string",
                            "description": "Update completion status - possible values: 'Yes', 'No'"
                        }
                    },
                    "required": ["WorkOrderNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWeldsbyNDEIndicationandWorkOrderNumber",
                "description": "Get welds for requested work order number filtered by specific NDE indication type. Both WorkOrderNumber and NDEIndication are required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "NDEIndication": {
                            "type": "string",
                            "description": "NDE indication type to filter by (e.g., Porosity, Concavity, Burn Through, etc.) - required"
                        }
                    },
                    "required": ["WorkOrderNumber", "NDEIndication"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWeldsbyTRIndicationandWorkOrderNumber",
                "description": "Get welds for requested work order number filtered by specific TR indication type. Both WorkOrderNumber and TRIndication are required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "TRIndication": {
                            "type": "string",
                            "description": "TR indication type to filter by (e.g., Porosity, Slag Inclusions, Foreign Material, Burn Through, Undercut, Other (enter in remarks), etc.) - required"
                        }
                    },
                    "required": ["WorkOrderNumber", "TRIndication"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetNDEReportProcessingDetailsbyWeldSerialNumber",
                "description": "Get list of all NDE report numbers and their type by requested weld serial number. WeldSerialNumber is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WeldSerialNumber": {
                            "type": "string",
                            "description": "Weld serial number (required)"
                        }
                    },
                    "required": ["WeldSerialNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetDetailsbyWeldSerialNumber",
                "description": "Get comprehensive weld details by weld serial number with optional filters. Returns structured data including Overall Details, Asset Details, CWI and NDE Result Details, and NDE Report Film Details. WeldSerialNumber is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WeldSerialNumber": {
                            "type": "string",
                            "description": "Weld serial number (required)"
                        },
                        "ProjectNumber": {
                            "type": "string",
                            "description": "Project number for additional filtering (optional)"
                        },
                        "HeatSerialNumber": {
                            "type": "string",
                            "description": "Heat serial number for additional filtering (optional)"
                        },
                        "NDEReportNumber": {
                            "type": "string",
                            "description": "NDE report number for additional filtering (optional)"
                        }
                    },
                    "required": ["WeldSerialNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetHeatNumberDetailsbyWorkOrderNumberandCriteria",
                "description": "Get heat number details for requested work order number with optional filtering criteria for material traceability. Returns heat numbers with asset, material, size, and manufacturer information. WorkOrderNumber is required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        },
                        "Asset": {
                            "type": "string",
                            "description": "Asset type filter (e.g., Pipe, Elbows, Weldolet, etc.) - optional"
                        },
                        "AssetSubcategory": {
                            "type": "string",
                            "description": "Asset subcategory filter (e.g., Seamless Line Pipe, Welded 22.5, etc.) - optional"
                        },
                        "Material": {
                            "type": "string",
                            "description": "Material type filter (e.g., Steel - GRADE X42, Steel - GRADE X52, etc.) - optional"
                        },
                        "Size": {
                            "type": "string",
                            "description": "Size specification filter (e.g., 12 NPS 0.375 SCH40, 4 NPS 0.237 SCH40, etc.) - optional"
                        },
                        "Manufacturer": {
                            "type": "string",
                            "description": "Manufacturer name filter (e.g., Tenaris Dalmine, TD Williamson, etc.) - optional"
                        }
                    },
                    "required": ["WorkOrderNumber"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrdersbyWelderName",
                "description": "Get list of work orders where there are welds made by a specific welder. Returns work order-level data with weld counts and serial numbers. WelderName is required. Accepts partial names.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WelderName": {
                            "type": "string",
                            "description": "Welder name (required). Accepts partial names (e.g., 'Vandaly' will match 'Vandaly Brian')"
                        }
                    },
                    "required": ["WelderName"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "GetWorkOrderSummary",
                "description": "Get comprehensive work order summary aggregating ALL data from multiple APIs. Performs complete server-side aggregation with 100% data coverage (no sampling). Returns full summary with weld statistics, welder performance, CWI/NDE/CRI inspection results, quality metrics, reshoot details, heat numbers, and exceptions. Use this for work order overview, summary, or report queries.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "WorkOrderNumber": {
                            "type": "string",
                            "description": "Work order number (required)"
                        }
                    },
                    "required": ["WorkOrderNumber"]
                }
            }
        }
    ]