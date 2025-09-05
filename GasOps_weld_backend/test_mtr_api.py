#!/usr/bin/env python3
"""
Test script for MTR API endpoints
Tests the GetMTRMetadataByCompanyMTRFileIDAndHeatNumber endpoint with different parameters
"""

import sys
import os
import json
from datetime import datetime, timezone, timedelta

# Add the current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import APIClient
from token_utils import generate_auth_token

def test_mtr_api():
    """Test the MTR API with different parameter combinations"""
    
    # Test credentials (same as used in the application)
    login_master_id = "1"
    database_name = "CEDEMONEW0314" 
    org_id = "CEDEMO "
    
    # Generate auth token
    auth_token = generate_auth_token(login_master_id, database_name, org_id)
    
    print("=== MTR API Test ===")
    print(f"Generated auth token: {auth_token}")
    print(f"Test time: {datetime.now()}")
    print()
    
    # Initialize API client
    try:
        api_client = APIClient()
        api_client.auth_token = auth_token
        print("[OK] API Client initialized successfully")
    except Exception as e:
        print(f"[ERROR] Failed to initialize API client: {e}")
        return
    
    # Test cases
    test_cases = [
        {
            "name": "Heat Number Only",
            "description": "Test with heat number 803KTEST001 and empty companyMTRFileID",
            "heat_number": "803KTEST001",
            "company_mtr_file_id": ""
        },
        {
            "name": "Heat Number + Company MTR File ID", 
            "description": "Test with heat number 803KTEST001 and companyMTRFileID 10045",
            "heat_number": "803KTEST001",
            "company_mtr_file_id": "10045"
        },
        {
            "name": "Heat Number + None Company MTR File ID",
            "description": "Test with heat number 803KTEST001 and None companyMTRFileID", 
            "heat_number": "803KTEST001",
            "company_mtr_file_id": None
        }
    ]
    
    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Heat Number: {test_case['heat_number']}")
        print(f"Company MTR File ID: {test_case['company_mtr_file_id']}")
        print("-" * 60)
        
        try:
            # Call the API
            result = api_client.get_mtr_metadata(
                test_case['company_mtr_file_id'], 
                test_case['heat_number']
            )
            
            # Display results
            print(f"[STATUS] API Call: {'SUCCESS' if result.get('success') else 'FAILED'}")
            print(f"[HTTP] Status Code: {result.get('status_code')}")
            
            if result.get('success'):
                print("[DATA] Response Data:")
                data = result.get('data')
                if isinstance(data, dict):
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                else:
                    print(f"   {data}")
                    
                # Check if it looks like valid MTR data
                if isinstance(data, dict):
                    if "Message" in data or "ModelState" in data:
                        print("[TYPE] ERROR MESSAGE")
                    else:
                        print("[TYPE] POSSIBLE MTR DATA")
                        
                        # Look for carbon-related fields
                        data_str = json.dumps(data).lower()
                        if "carbon" in data_str or "c:" in data_str or "chemical" in data_str:
                            print("[CONTENT] Contains chemical/carbon information")
                        else:
                            print("[CONTENT] No obvious chemical composition found")
                else:
                    print("[TYPE] STRING/OTHER")
            else:
                print(f"[ERROR] {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"[EXCEPTION] {str(e)}")
            print(f"   Exception type: {type(e).__name__}")
    
    print(f"\n{'='*60}")
    print("[COMPLETE] Test Complete!")
    print(f"Test completed at: {datetime.now()}")

def main():
    """Main function"""
    print("Starting MTR API Test...")
    test_mtr_api()

if __name__ == "__main__":
    main()