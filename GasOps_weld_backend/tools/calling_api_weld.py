# Weld API Integration Module
# Provides unified interface for calling external welding management system APIs
# Handles certificate-based authentication and request/response processing

import requests
import requests_pkcs12
import tempfile
import base64
import os

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
    # Log API call for debugging (remove auth token logging in production for security)
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"Calling Weld API '{api_name}' with {len(payload)} parameters")
    
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
        
        # Determine HTTP method based on API (keeping original logic)
        if api_name in ["GetMTRFileDatabyHeatNumber", "GetWeldDetailsByWeldSerialNumber", 
                       "GetMaterialAssetsByWeldSerialNumber", "GetJoinersByWeldSerialNumber",
                       "GetVisualInspectionResultsByWeldSerialNumber"]:
            # GET request with query parameters
            response = requests_pkcs12.get(
                url,
                headers=headers,
                params=payload,
                pkcs12_data=pfx_data,
                pkcs12_password="password1234"
            )
        else:
            # POST request with JSON body
            response = requests_pkcs12.post(
                url,
                headers=headers,
                json=payload,
                pkcs12_data=pfx_data,
                pkcs12_password="password1234"
            )
        
        try:
            result = response.json()
            return {"success": True, "data": result, "status_code": response.status_code}
        except Exception:
            return {"success": True, "data": response.text, "status_code": response.status_code}
            
    except Exception as e:
        return {"error": str(e)}
    finally:
        if temp_file:
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass