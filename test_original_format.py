#!/usr/bin/env python3
"""
Test the backend with original frontend format
"""
import requests
import json

def test_original_format():
    """Test backend with original frontend request format"""
    print("Testing Original Frontend Format")
    print("=" * 40)
    
    # Original frontend request format
    payload = {
        "query": "Show me work order WR12345",
        "token": "MSZDRURFTU9ORVcwMzE0JkNFREVNTyA=",  # CEDEMO token
        "session_id": None,
        "prev_msgs": None
    }
    
    headers = {
        "Content-Type": "application/json",
        "encoded-string": "MSZDRURFTU9ORVcwMzE0JkNFREVNTyA="  # Same token in header
    }
    
    print(f"Request payload: {payload}")
    print(f"Headers: {headers}")
    print()
    
    try:
        print("Sending request to backend...")
        response = requests.post(
            "http://localhost:8000/ask",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS: Backend responded")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to backend")
        print("Make sure the backend is running: python GasOps_weld_backend/app.py")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_original_format()