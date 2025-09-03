"""
Industrial API Client for connecting to all the industrial system APIs
"""
import requests_pkcs12
import tempfile
import os
import base64
import json
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the API client and generate the authentication token.
        """
        # Load credentials from environment variables
        self.base_url = base_url or os.environ.get("BASE_URL")
        self.pfx_source = os.environ.get("PFX_SOURCE")
        self.pfx_password = os.environ.get("PFX_PASSWORD")
        self.login_master_id = os.environ.get("AUTH_TOKEN_LOGIN_MASTER_ID")
        self.database_name = os.environ.get("AUTH_TOKEN_DATABASE_NAME")
        self.org_id = os.environ.get("AUTH_TOKEN_ORG_ID")
        
        if not all([self.base_url, self.pfx_source, self.pfx_password, self.login_master_id, self.database_name, self.org_id]):
            raise ValueError("All required environment variables must be set.")

        self.base_url = self.base_url.rstrip('/')
        self.temp_file = None
        
        self.auth_token = self._generate_auth_token()
        
    def _generate_auth_token(self):
        """Generates an authentication token based on class attributes."""
        now_utc = datetime.now(timezone.utc)
        date_plus_one = (now_utc + timedelta(days=1)).isoformat()
        date_now = now_utc.isoformat()
        
        token_str = f"{date_plus_one}&{self.login_master_id}&{self.database_name}&{date_now}&{self.org_id}"
        return base64.b64encode(token_str.encode('utf-8')).decode('utf-8')
    
    def _prepare_certificate(self):
        """Prepare the certificate for use"""
        try:
            # If the input is a base64 string (not a file path), decode and save as temp file
            if not os.path.isfile(self.pfx_source):
                try:
                    cert_bytes = base64.b64decode(self.pfx_source)
                except Exception as decode_err:
                    raise Exception(f"Failed to decode base64 certificate: {decode_err}")
                
                self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pfx")
                self.temp_file.write(cert_bytes)
                self.temp_file.close()
                pfx_path = self.temp_file.name
            else:
                pfx_path = self.pfx_source
                
            with open(pfx_path, "rb") as f:
                pfx_data = f.read()
                
            return pfx_data
        except Exception as e:
            raise Exception(f"Failed to prepare certificate: {str(e)}")
    
    def _cleanup_certificate(self):
        """Clean up temporary certificate file"""
        if self.temp_file:
            try:
                os.unlink(self.temp_file.name)
                self.temp_file = None
            except Exception:
                pass
    
    def _make_request(self, method: str, endpoint: str, 
                      params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an API request. The auth token is handled internally.
        """
        try:
            pfx_data = self._prepare_certificate()
            
            url = f"{self.base_url}{endpoint}"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "auth-token": self.auth_token # Use the internally stored token
            }
            
            logger.info(f"Making {method} request to {url}")
            if params:
                logger.info(f"Query params: {params}")
            if json_data:
                logger.info(f"JSON data: {json_data}")
            
            if method.upper() == 'GET':
                response = requests_pkcs12.get(
                    url,
                    headers=headers,
                    params=params,
                    pkcs12_data=pfx_data,
                    pkcs12_password=self.pfx_password,
                    timeout=30
                )
            elif method.upper() == 'POST':
                response = requests_pkcs12.post(
                    url,
                    headers=headers,
                    params=params,
                    json=json_data,
                    pkcs12_data=pfx_data,
                    pkcs12_password=self.pfx_password,
                    timeout=30
                )
            else:
                raise Exception(f"Unsupported HTTP method: {method}")
            
            logger.info(f"Response status: {response.status_code}")
            
            try:
                result = response.json()
                return {
                    "success": True,
                    "data": result,
                    "status_code": response.status_code
                }
            except json.JSONDecodeError:
                return {
                    "success": response.status_code == 200,
                    "data": response.text,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            self._cleanup_certificate()
    
    # MTR/Material APIs
    def get_mtr_metadata(self, company_mtr_file_id: str, heat_number: str) -> Dict[str, Any]:
        """Get MTR Metadata by CompanyMTRFileID and HeatNumber"""
        params = {
            "companyMTRFileID": company_mtr_file_id,
            "heatNumber": heat_number
        }
        return self._make_request(
            "GET", 
            "/api/AIMTRMetaData/GetMTRMetadataByCompanyMTRFileIDAndHeatNumber",
            params=params
        )
    
    def add_update_mtr_metadata(self, mtr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add or Update MTR Metadata"""
        return self._make_request(
            "POST",
            "/api/AIMTRMetaData/AddUpdateMTRMetadata",
            json_data=mtr_data
        )
    
    # Work Order API
    def get_work_order_information(self, wr_number: str) -> Dict[str, Any]:
        """Get WorkOrder Information and Assignment"""
        json_data = {"WRNumber": wr_number}
        return self._make_request(
            "POST",
            "/api/AITransmissionWorkOrder/GetWorkOrderInformationAndAssignment",
            json_data=json_data
        )
    
    # Weld APIs
    def get_all_weld_details_by_work_order(self, wr_number: str) -> Dict[str, Any]:
        """Get All Weld Details by WorkOrder"""
        json_data = {"WRNumber": wr_number}
        return self._make_request(
            "POST",
            "/api/AITransmissionWorkOrder/GetAllWeldDetailsByWorkOrder",
            json_data=json_data
        )
    
    def get_material_assets_by_weld_serial_number(self, weld_serial_number: str) -> Dict[str, Any]:
        """Get Material Assets by WeldSerialNumber"""
        params = {"WeldSerialNumber": weld_serial_number}
        return self._make_request(
            "GET",
            "/api/AITransmissionWorkOrder/GetMaterialAssetsByWeldSerialNumber",
            params=params
        )
    
    def get_joiners_by_weld_serial_number(self, weld_serial_number: str) -> Dict[str, Any]:
        """Get Joiners by WeldSerialNumber"""
        params = {"WeldSerialNumber": weld_serial_number}
        return self._make_request(
            "GET",
            "/api/AITransmissionWorkOrder/GetJoinersByWeldSerialNumber",
            params=params
        )
    
    def get_visual_inspection_results_by_weld_serial_number(self, weld_serial_number: str) -> Dict[str, Any]:
        """Get Visual Inspection Results by WeldSerialNumber"""
        params = {"WeldSerialNumber": weld_serial_number}
        return self._make_request(
            "GET",
            "/api/AITransmissionWorkOrder/GetVisualInspectionResultsByWeldSerialNumber",
            params=params
        )
    
    def get_weld_details_by_weld_serial_number(self, weld_serial_number: str) -> Dict[str, Any]:
        """Get Weld Details by WeldSerialNumber"""
        params = {"WeldSerialNumber": weld_serial_number}
        return self._make_request(
            "GET",
            "/api/AITransmissionWorkOrder/GetWeldDetailsByWeldSerialNumber",
            params=params
        )
    
    def get_nde_and_cri_inspection_details(self, wr_number: str, weld_id: str) -> Dict[str, Any]:
        """Get NDE and CRI Inspection Details"""
        json_data = {
            "WRNumber": wr_number,
            "WeldID": weld_id
        }
        return self._make_request(
            "POST",
            "/api/AITransmissionWorkOrder/GetNDEAndCRIInspectionDetailsByWeldSerialNumberAndWRNumber",
            json_data=json_data
        )
    
    def get_nde_cri_and_tertiary_inspection_details(self, wr_number: str, weld_id: str) -> Dict[str, Any]:
        """Get NDE, CRI and Tertiary Inspection Details"""
        json_data = {
            "WRNumber": wr_number,
            "WeldID": weld_id
        }
        return self._make_request(
            "POST",
            "/api/AITransmissionWorkOrder/GetNDECRIAndTertiaryInspectionDetailsByWeldSerialNumberAndWRNumber",
            json_data=json_data
        )