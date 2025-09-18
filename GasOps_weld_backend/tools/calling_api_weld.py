# Weld API Integration Module
# Provides unified interface for calling external welding management system APIs
# Handles certificate-based authentication and request/response processing

import requests
import requests_pkcs12
import tempfile
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def call_weld_api(api_name, parameters, auth_token, pfx_source="./certificate/oamsapicert2023.pfx"):
    """
    Universal API client for external welding management system endpoints.
    
    Provides secure, certificate-based authentication for accessing welding data APIs.
    Supports both GET and POST requests with automatic method selection based on API type.
    
    Args:
        api_name (str): API endpoint identifier (e.g., 'GetMTRFileDatabyHeatNumber')
        parameters (dict): Request parameters specific to the API endpoint
        auth_token (str): Authentication token for request authorization
        pfx_source (str): Path to .pfx certificate file or base64 certificate string
        
    Returns:
        dict: Standardized response with success status, data, and HTTP status code
              Format: {"success": bool, "data": any, "status_code": int}
              Error format: {"error": str}
              
    Security Features:
    - PKCS#12 certificate-based client authentication
    - Secure temporary file handling for certificates
    - Automatic certificate cleanup after use
    - HTTPS-only communication with external APIs
    
    Supported API Categories:
    - MTR (Material Test Report) data retrieval
    - Work order information and assignments  
    - Weld details and serial number tracking
    - Material assets and joiner information
    - Inspection results (Visual, NDE, CRI, Tertiary)
    """
    
    # Map API names to endpoints (keeping original endpoints)
    api_endpoints = {
        "GetMTRFileDatabyHeatNumber": "/api/AIMTRMetaData/GetMTRFileDatabyHeatNumber",
        "GetAllWeldDetailsByWorkOrder": "/api/AITransmissionWorkOrder/GetAllWeldDetailsByWorkOrder", 
        "GetWorkOrderInformationAndAssignment": "/api/AITransmissionWorkOrder/GetWorkOrderInformationAndAssignment",
        "GetWeldDetailsByWeldSerialNumber": "/api/AITransmissionWorkOrder/GetWeldDetailsByWeldSerialNumber",
        "GetMaterialAssetsByWeldSerialNumber": "/api/AITransmissionWorkOrder/GetMaterialAssetsByWeldSerialNumber",
        "GetJoinersByWeldSerialNumber": "/api/AITransmissionWorkOrder/GetJoinersByWeldSerialNumber",
        "GetVisualInspectionResultsByWeldSerialNumber": "/api/AITransmissionWorkOrder/GetVisualInspectionResultsByWeldSerialNumber",
        "GetNDEAndCRIInspectionDetailsByWeldSerialNumberAndWRNumber": "/api/AITransmissionWorkOrder/GetNDEAndCRIInspectionDetailsByWeldSerialNumberAndWRNumber",
        "GetNDECRIAndTertiaryInspectionDetailsByWeldSerialNumberAndWRNumber": "/api/AITransmissionWorkOrder/GetNDECRIAndTertiaryInspectionDetailsByWeldSerialNumberAndWRNumber"
    }
    
    endpoint = api_endpoints.get(api_name)
    if not endpoint:
        return {"error": f"Unknown API: {api_name}"}
    
    url = f"https://oamsapi.gasopsiq.com{endpoint}"
    payload = parameters
    # Enhanced debugging for API calls
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"=== WELD API CALL ===")
    logger.info(f"API Name: {api_name}")
    logger.info(f"Endpoint: {endpoint}")
    logger.info(f"URL: https://oamsapi.gasopsiq.com{endpoint}")
    logger.info(f"Parameters: {payload}")
    logger.info(f"Parameter count: {len(payload)}")
    logger.info(f"Auth token provided: {bool(auth_token)}")
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "auth-token": auth_token
    }
    
    temp_file = None
    try:
        # If the input is a base64 string (not a file path), decode and save as temp file
        if not os.path.isfile(pfx_source):
            try:
                cert_bytes = base64.b64decode(pfx_source)
            except Exception as decode_err:
                return {"error": f"Failed to decode base64 certificate: {decode_err}"}
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pfx")
            temp_file.write(cert_bytes)
            temp_file.close()
            pfx_path = temp_file.name
        else:
            pfx_path = pfx_source
            
        with open(pfx_path, "rb") as f:
            pfx_data = f.read()
        
        # Determine HTTP method based on API specifications
        # GET APIs: Only MTR-related APIs use GET requests with query parameters
        logger.info(f"=== DETERMINING HTTP METHOD ===")
        if api_name in ["GetMTRFileDatabyHeatNumber"]:
            # GET request with query parameters
            logger.info(f"Using GET method for MTR API")
            logger.info(f"Query parameters: {payload}")
            response = requests_pkcs12.get(
                url,
                headers=headers,
                params=payload,
                pkcs12_data=pfx_data,
                pkcs12_password=os.getenv("PFX_PASSWORD")
            )
        else:
            # POST APIs: All WeldInsight APIs use POST requests with JSON body
            # WeldInsight APIs: GetWorkOrderInformationAndAssignment, GetAllWeldDetailsByWorkOrder,
            # GetWeldDetailsByWeldSerialNumber, GetMaterialAssetsByWeldSerialNumber,
            # GetJoinersByWeldSerialNumber, GetVisualInspectionResultsByWeldSerialNumber,
            # GetNDEAndCRIInspectionDetailsByWeldSerialNumberAndWRNumber, GetNDECRIAndTertiaryInspectionDetailsByWeldSerialNumberAndWRNumber
            # POST request with JSON body
            logger.info(f"Using POST method for WeldInsight API")
            logger.info(f"JSON payload: {payload}")
            response = requests_pkcs12.post(
                url,
                headers=headers,
                json=payload,
                pkcs12_data=pfx_data,
                pkcs12_password=os.getenv("PFX_PASSWORD")
            )

        logger.info(f"=== API RESPONSE ===")
        logger.info(f"Status code: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        logger.info(f"Response size: {len(response.content) if response.content else 0} bytes")
        
        try:
            result = response.json()
            logger.info(f"=== PARSED JSON RESPONSE ===")
            logger.info(f"Result type: {type(result)}")
            if isinstance(result, dict):
                logger.info(f"Result keys: {list(result.keys())}")
                if 'Obj' in result:
                    obj_data = result['Obj']
                    logger.info(f"'Obj' field type: {type(obj_data)}")
                    if isinstance(obj_data, list):
                        logger.info(f"'Obj' contains {len(obj_data)} items")
                        if obj_data:
                            logger.info(f"First item keys: {list(obj_data[0].keys()) if isinstance(obj_data[0], dict) else 'Not a dict'}")
                    elif obj_data is None:
                        logger.info(f"'Obj' field is None - no data found")
                    else:
                        logger.info(f"'Obj' field content: {obj_data}")
                else:
                    logger.info(f"No 'Obj' field in response")
            elif isinstance(result, list):
                logger.info(f"Result is list with {len(result)} items")
            else:
                logger.info(f"Result content: {str(result)[:200]}...")

            return {"success": True, "data": result, "status_code": response.status_code}
        except Exception as json_error:
            logger.warning(f"Failed to parse JSON response: {str(json_error)}")
            logger.warning(f"Raw response text: {response.text[:500]}...")
            return {"success": True, "data": response.text, "status_code": response.status_code}
            
    except Exception as e:
        return {"error": str(e)}
    finally:
        if temp_file:
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass