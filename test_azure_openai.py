#!/usr/bin/env python3
"""
Test Azure OpenAI connection
"""
import asyncio
import os
import sys

# Add backend to path
sys.path.append('./GasOps_weld_backend')

from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv('./GasOps_weld_backend/.env')

def test_azure_openai():
    """Test Azure OpenAI connection and query classification"""
    print("Testing Azure OpenAI Connection")
    print("=" * 40)
    
    # Print configuration
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    print(f"Endpoint: {endpoint}")
    print(f"API Key: {api_key[:20] if api_key else 'None'}...")
    print(f"Deployment: {deployment}")
    print(f"API Version: {api_version}")
    print()
    
    try:
        # Initialize client
        print("1. Initializing Azure OpenAI client...")
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        print("   SUCCESS: Client initialized")
        print()
        
        # Test simple completion
        print("2. Testing simple completion...")
        test_query = "Get work order information for WR Number 280489410001"
        
        prompt = f"""
Analyze this query and respond with JSON only:

Query: "{test_query}"

Determine:
1. Type: "work_order", "weld", or "mtr" 
2. Extract parameters like WRNumber, ProjectNumber, etc.

JSON format:
{{
  "type": "work_order",
  "parameters": {{"wr_number": "123"}}
}}
"""
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a query classifier. Respond only with JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        result = response.choices[0].message.content.strip()
        print(f"   SUCCESS: Got response: {result}")
        
        # Try to parse JSON
        import json
        try:
            parsed = json.loads(result)
            print(f"   SUCCESS: JSON parsed: {parsed}")
        except Exception as e:
            print(f"   WARNING: JSON parse error: {e}")
        
        print()
        print("SUCCESS: Azure OpenAI connection is working!")
        
    except Exception as e:
        print(f"FAILED: Azure OpenAI test failed!")
        print(f"Error: {str(e)}")
        print("Check your configuration and network connectivity")

if __name__ == "__main__":
    test_azure_openai()