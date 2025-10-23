import logging
from collections import defaultdict
import json
from utils.weld_api_data_processor.GetHeatNumberDetailsbyWorkOrderNumberandCriteria import analyze_GetHeatNumberDetailsbyWorkOrderNumberandCriteria
from utils.weld_api_data_processor.GetDetailsbyWeldSerialNumber import analyze_GetDetailsbyWeldSerialNumber
from utils.weld_api_data_processor.GetNDEReportNumbersbyWorkOrderNumber import analyze_GetNDEReportNumbersbyWorkOrderNumber
from utils.weld_api_data_processor.GetNDEReportProcessingDetailsbyWeldSerialNumber import analyze_GetNDEReportProcessingDetailsbyWeldSerialNumber
from utils.weld_api_data_processor.GetReshootDetailsbyWorkOrderNumberandCriteria import analyze_GetReshootDetailsbyWorkOrderNumberandCriteria   
from utils.weld_api_data_processor.GetUnlockWeldDetailsbyWorkOrderNumberandCriteria import analyze_GetUnlockWeldDetailsbyWorkOrderNumberandCriteria
from utils.weld_api_data_processor.GetWeldDetailsbyWorkOrderNumberandCriteria import analyze_GetWeldDetailsbyWorkOrderNumberandCriteria
from utils.weld_api_data_processor.GetWelderNameDetailsbyWorkOrderNumberandCriteria import analyze_GetWelderNameDetailsbyWorkOrderNumberandCriteria
from utils.weld_api_data_processor.GetWeldsbyNDEIndicationandWorkOrderNumber import analyze_GetWeldsbyNDEIndicationandWorkOrderNumber
from utils.weld_api_data_processor.GetWorkOrderDetailsbyCriteria import analyze_GetWorkOrderDetailsbyCriteria
from utils.weld_api_data_processor.GetWorkOrderInformation import analyze_GetWorkOrderInformation
from utils.weld_api_data_processor.GetWorkOrderNDEIndicationsbyCriteria import analyze_GetWorkOrderNDEIndicationsbyCriteria
from utils.weld_api_data_processor.GetWorkOrderRejactableNDEIndicationsbyCriteria import analyze_GetWorkOrderRejactableNDEIndicationsbyCriteria
from utils.weld_api_data_processor.GetWorkOrdersbyWelderName import analyze_GetWorkOrdersbyWelderName

logger = logging.getLogger(__name__)


def get_transformer(api_name):
    """
    Acts as a router to get the correct data transformer for an API.
    This pattern makes it easy to add support for new APIs.
    """
    if api_name == "GetHeatNumberDetailsbyWorkOrderNumberandCriteria":
        return analyze_GetHeatNumberDetailsbyWorkOrderNumberandCriteria
    elif api_name == "GetDetailsbyWeldSerialNumber":
        return analyze_GetDetailsbyWeldSerialNumber
    elif api_name == "GetNDEReportNumbersbyWorkOrderNumber":
        return analyze_GetNDEReportNumbersbyWorkOrderNumber
    elif api_name == "GetNDEReportProcessingDetailsbyWeldSerialNumber":
        return analyze_GetNDEReportProcessingDetailsbyWeldSerialNumber
    elif api_name == "GetReshootDetailsbyWorkOrderNumberandCriteria":
        return analyze_GetReshootDetailsbyWorkOrderNumberandCriteria
    elif api_name == "GetUnlockWeldDetailsbyWorkOrderNumberandCriteria":
        return analyze_GetUnlockWeldDetailsbyWorkOrderNumberandCriteria
    elif api_name == "GetWeldDetailsbyWorkOrderNumberandCriteria":
        return analyze_GetWeldDetailsbyWorkOrderNumberandCriteria
    elif api_name == "GetWelderNameDetailsbyWorkOrderNumberandCriteria":
        return analyze_GetWelderNameDetailsbyWorkOrderNumberandCriteria
    elif api_name == "GetWeldsbyNDEIndicationandWorkOrderNumber":
        return analyze_GetWeldsbyNDEIndicationandWorkOrderNumber
    elif api_name == "GetWorkOrderDetailsbyCriteria":
        return analyze_GetWorkOrderDetailsbyCriteria
    elif api_name == "GetWorkOrderInformation":
        return analyze_GetWorkOrderInformation
    elif api_name == "GetWorkOrderNDEIndicationsbyCriteria":
        return analyze_GetWorkOrderNDEIndicationsbyCriteria
    elif api_name == "GetWorkOrderRejactableNDEIndicationsbyCriteria":
        return analyze_GetWorkOrderRejactableNDEIndicationsbyCriteria
    elif api_name == "GetWorkOrdersbyWelderName":
        return analyze_GetWorkOrdersbyWelderName
    # Add other API transformers here
    # elif api_name == "GetWorkOrderInformation":
    #     return analyze_work_order_data
    else:
        logger.warning(f"No specific transformer found for API: {api_name}")
        return None
