import asyncio
import aiohttp
import json
from tools.execute_api import execute_api
from utils.weld_api_data_processor.WorkOrderSummary import analyze_WorkOrderSummary

async def async_execute_api(api_path, function_name, parameters, auth_token):
    """
    An asynchronous wrapper for the existing synchronous API execution function.
    Runs the API call in a separate thread to prevent blocking.
    """
    return await asyncio.to_thread(
        execute_api,
        api_path,
        function_name,
        parameters,
        auth_token,
        method="POST"
    )

async def orchestrate_work_orderSummary_async(work_order_number, auth_token):
    """
    Orchestrates parallel API calls and returns the combined, preprocessed data.
    """
    api_path = "AITransmissionWorkOrder"
    
    tasks = [
        async_execute_api(api_path, "GetWorkOrderInformation", {"WorkOrderNumber": work_order_number}, auth_token),
        async_execute_api(api_path, "GetWeldDetailsbyWorkOrderNumberandCriteria", {"WorkOrderNumber": work_order_number}, auth_token)
    ]
    
    # Execute both API calls in parallel
    results = await asyncio.gather(*tasks)

    # Combine results into a structured format
    api_results = [
        {"api_name": "GetWorkOrderInformation", "data": results[0]},
        {"api_name": "GetWeldDetailsbyWorkOrderNumberandCriteria", "data": results[1]}
    ]

    # Pre-process the raw results using a dedicated transformer
    # This function will handle all the extraction and aggregation
    return analyze_WorkOrderSummary(api_results, {"WorkOrderNumber": work_order_number})

def orchestrate_work_orderSummary(work_order_number, auth_token):
    """
    Synchronous wrapper to run the asynchronous orchestration logic.
    """
    return asyncio.run(orchestrate_work_orderSummary_async(work_order_number, auth_token))