#!/usr/bin/env python3
"""
Test script to verify frontend-backend connection
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.append('./GasOps_weld_backend')

from app import generate_auth_token
from orchestrator_agent import OrchestratorAgent

async def test_connection():
    """Test the connection with sample data"""
    print("Testing Frontend-Backend Connection")
    print("=" * 50)
    
    # Test credentials (matching frontend App.js CEDEMO config)
    test_org_id = "CEDEMO"
    test_database = "CEDEMO"  
    test_master_id = "test_login"
    test_query = "Get work order information for WR Number 280489410001"
    
    print(f"Test Credentials:")
    print(f"   - orgID: {test_org_id}")
    print(f"   - databasename: {test_database}")
    print(f"   - masterID: {test_master_id}")
    print(f"   - query: {test_query}")
    print()
    
    try:
        # 1. Test auth token generation
        print("1. Testing Auth Token Generation...")
        auth_token = generate_auth_token(test_org_id, test_database, test_master_id)
        print(f"   SUCCESS: Auth token generated: {auth_token[:20]}...")
        print()
        
        # 2. Test orchestrator processing
        print("2. Testing Orchestrator Processing...")
        orchestrator = OrchestratorAgent()
        result = await orchestrator.process(test_query, auth_token)
        
        print("Result:")
        print(f"   - Success: {result.get('success', False)}")
        print(f"   - Agent: {result.get('agent', 'N/A')}")
        print(f"   - AI Classification: {result.get('ai_classification', {})}")
        
        if result.get('error'):
            print(f"   - Error: {result.get('error')}")
        
        if result.get('data'):
            print(f"   - Data Length: {len(str(result.get('data', {})))} chars")
        
        print()
        
        if result.get('success'):
            print("SUCCESS: Connection test PASSED!")
            print("Frontend and backend should work together!")
        else:
            print("WARNING: Connection test completed with errors")
            print("Check your API configuration and credentials")
            
    except Exception as e:
        print(f"FAILED: Connection test failed!")
        print(f"Error: {str(e)}")
        print("Check your backend configuration")

if __name__ == "__main__":
    asyncio.run(test_connection())