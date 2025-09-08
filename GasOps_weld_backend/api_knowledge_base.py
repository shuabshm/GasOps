"""
Comprehensive API Knowledge Base for GasOps Weld Management System
Contains all API details, parameters, and routing logic for both MTR and WeldInsight agents
"""

# Complete API Knowledge Base
API_KNOWLEDGE_BASE = {
    # MTR Agent - Single API
    "mtr_file_data": {
        "description": "Get MTR (Material Test Report) file data and properties by heat number",
        "api_endpoint": "/api/AIMTRMetaData/GetMTRFileDatabyHeatNumber",
        "method": "get_mtr_file_data_by_heat_number",
        "required_params": ["heat_number"],
        "optional_params": ["company_mtr_file_id"],
        "param_format": {
            "heat_number": "string - Material heat number identifier",
            "company_mtr_file_id": "string (optional) - Company MTR file identifier"
        },
        "example_questions": [
            "What are the properties of heat number 18704220?",
            "Show me MTR data for heat W4A789",
            "Get material properties for this heat number",
            "What's the chemical composition of heat 12345?",
            "Show me the MTR file for heat ABC123",
            "Get material specifications for this heat"
        ],
        "keywords": ["MTR", "material", "heat number", "heat", "properties", "composition", "grade", "specification", "test report"],
        "http_method": "GET",
        "agent": "MTR"
    },
    
    # WeldInsight Agent - All Weld Related APIs
    "weld_details_by_work_order": {
        "description": "Get all weld details for a specific work order",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetAllWeldDetailsByWorkOrder",
        "method": "get_all_weld_details_by_work_order",
        "required_params": ["wr_number"],
        "optional_params": [],
        "param_format": {
            "wr_number": "string - Work order number"
        },
        "example_questions": [
            "Show me all welds for work order 12345",
            "What welds are in WR 67890?",
            "List welding details for work order ABC123",
            "Get weld information for this job",
            "Show me welds for this work order"
        ],
        "keywords": ["all welds", "work order welds", "WR welds", "job welds", "work order", "WR"],
        "http_method": "POST",
        "agent": "WeldInsight"
    },
    
    "work_order_information": {
        "description": "Get work order information and assignment details",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetWorkOrderInformationAndAssignment",
        "method": "get_work_order_information",
        "required_params": ["wr_number"],
        "optional_params": [],
        "param_format": {
            "wr_number": "string - Work order number"
        },
        "example_questions": [
            "What is work order 12345?",
            "Show me WR details for 67890",
            "Get information about work order ABC123",
            "Tell me about this work order",
            "Show work order assignment"
        ],
        "keywords": ["work order info", "WR info", "work order details", "assignment", "job info"],
        "http_method": "POST",
        "agent": "WeldInsight"
    },
    
    "weld_details_by_serial": {
        "description": "Get specific weld details by weld serial number",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetWeldDetailsByWeldSerialNumber",
        "method": "get_weld_details_by_weld_serial_number",
        "required_params": ["weld_serial_number"],
        "optional_params": [],
        "param_format": {
            "weld_serial_number": "string - Weld serial number identifier"
        },
        "example_questions": [
            "Show me weld details for serial number W123",
            "Get weld information for serial ABC456",
            "What are the details of weld W789?",
            "Show me this specific weld"
        ],
        "keywords": ["weld serial", "weld number", "specific weld", "weld details", "serial number"],
        "http_method": "GET",
        "agent": "WeldInsight"
    },
    
    "material_assets_by_weld": {
        "description": "Get material assets associated with a specific weld",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetMaterialAssetsByWeldSerialNumber",
        "method": "get_material_assets_by_weld_serial_number",
        "required_params": ["weld_serial_number"],
        "optional_params": [],
        "param_format": {
            "weld_serial_number": "string - Weld serial number"
        },
        "example_questions": [
            "What materials are used in weld W123?",
            "Show me material assets for this weld",
            "Get materials for weld serial ABC456",
            "What assets are in this weld?"
        ],
        "keywords": ["material assets", "weld materials", "assets", "materials", "weld components"],
        "http_method": "GET",
        "agent": "WeldInsight"
    },
    
    "joiners_by_weld": {
        "description": "Get joiner information for a specific weld",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetJoinersByWeldSerialNumber",
        "method": "get_joiners_by_weld_serial_number",
        "required_params": ["weld_serial_number"],
        "optional_params": [],
        "param_format": {
            "weld_serial_number": "string - Weld serial number"
        },
        "example_questions": [
            "Who welded this joint W123?",
            "Show me joiners for weld ABC456",
            "Get welder information for this weld",
            "Who performed this weld?"
        ],
        "keywords": ["joiners", "welders", "who welded", "welder info", "personnel"],
        "http_method": "GET",
        "agent": "WeldInsight"
    },
    
    "visual_inspection_results": {
        "description": "Get visual inspection results for a specific weld",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetVisualInspectionResultsByWeldSerialNumber",
        "method": "get_visual_inspection_results_by_weld_serial_number",
        "required_params": ["weld_serial_number"],
        "optional_params": [],
        "param_format": {
            "weld_serial_number": "string - Weld serial number"
        },
        "example_questions": [
            "What are the visual inspection results for weld W123?",
            "Show me inspection results for this weld",
            "Get visual inspection data for weld ABC456",
            "Did this weld pass visual inspection?"
        ],
        "keywords": ["visual inspection", "inspection results", "visual test", "inspection", "VT"],
        "http_method": "GET",
        "agent": "WeldInsight"
    },
    
    "nde_cri_inspection": {
        "description": "Get NDE (Non-Destructive Examination) and CRI inspection details",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetNDEAndCRIInspectionDetailsByWeldSerialNumberAndWRNumber",
        "method": "get_nde_and_cri_inspection_details",
        "required_params": ["wr_number", "weld_id"],
        "optional_params": [],
        "param_format": {
            "wr_number": "string - Work order number",
            "weld_id": "string - Weld identifier"
        },
        "example_questions": [
            "Show me NDE results for this weld",
            "What are the CRI inspection details?",
            "Get non-destructive test results",
            "Show me radiographic test results",
            "What are the ultrasonic test results?"
        ],
        "keywords": ["NDE", "CRI", "non-destructive", "radiographic", "ultrasonic", "RT", "UT", "inspection"],
        "http_method": "POST",
        "agent": "WeldInsight"
    },
    
    "nde_cri_tertiary_inspection": {
        "description": "Get NDE, CRI and Tertiary inspection details",
        "api_endpoint": "/api/AITransmissionWorkOrder/GetNDECRIAndTertiaryInspectionDetailsByWeldSerialNumberAndWRNumber",
        "method": "get_nde_cri_and_tertiary_inspection_details",
        "required_params": ["wr_number", "weld_id"],
        "optional_params": [],
        "param_format": {
            "wr_number": "string - Work order number",
            "weld_id": "string - Weld identifier"
        },
        "example_questions": [
            "Show me all inspection results for this weld",
            "Get complete inspection details",
            "What are all the test results?",
            "Show me tertiary inspection results",
            "Get full inspection report"
        ],
        "keywords": ["all inspections", "complete inspection", "tertiary", "full inspection", "all tests"],
        "http_method": "POST",
        "agent": "WeldInsight"
    }
}

# Agent-specific keyword mappings for fast classification
MTR_KEYWORDS = [
    "MTR", "material", "heat number", "heat", "properties", "composition", 
    "grade", "specification", "test report", "chemical", "mechanical"
]

WELD_KEYWORDS = [
    "weld", "welding", "work order", "WR", "job", "joint", "pipe", 
    "inspection", "serial", "joiner", "welder", "visual", "NDE", "CRI", 
    "radiographic", "ultrasonic", "RT", "UT", "assets", "materials"
]

def get_agent_apis(agent_name):
    """Get all APIs for a specific agent"""
    return {k: v for k, v in API_KNOWLEDGE_BASE.items() if v["agent"] == agent_name}

def get_api_by_keywords(query):
    """Quick keyword-based API selection"""
    query_lower = query.lower()
    
    # Check for MTR keywords first
    if any(keyword.lower() in query_lower for keyword in MTR_KEYWORDS):
        return "mtr_file_data"
    
    # Check for specific weld API keywords
    api_scores = {}
    for api_name, config in API_KNOWLEDGE_BASE.items():
        if config["agent"] == "WeldInsight":
            score = sum(1 for keyword in config["keywords"] if keyword.lower() in query_lower)
            if score > 0:
                api_scores[api_name] = score
    
    if api_scores:
        return max(api_scores, key=api_scores.get)
    
    # Default fallbacks
    if any(keyword in query_lower for keyword in ["work order", "wr"]):
        return "work_order_information"
    
    return "weld_details_by_work_order"  # Default weld API

def get_required_params(api_name):
    """Get required parameters for an API"""
    return API_KNOWLEDGE_BASE.get(api_name, {}).get("required_params", [])

def get_api_description(api_name):
    """Get full description of an API"""
    config = API_KNOWLEDGE_BASE.get(api_name, {})
    return f"""
API: {api_name}
Description: {config.get('description', '')}
Required Parameters: {config.get('required_params', [])}
Optional Parameters: {config.get('optional_params', [])}
Example Questions: {config.get('example_questions', [])}
"""