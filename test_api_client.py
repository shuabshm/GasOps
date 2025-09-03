import os
import asyncio
import json
from GasOps_weld_backend.api_client import APIClient

async def test_all_apis():
    """Test all API endpoints with sample data."""
    try:
        # Client now initializes without parameters, pulling from .env
        client = APIClient()
    except ValueError as e:
        print(f"❌ Error initializing client: {e}")
        return

    print("🔧 Testing Industrial APIs...")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Work Order Information",
            "function": lambda: client.get_work_order_information("100139423P2"),
        },
        {
            "name": "All Weld Details by Work Order",
            "function": lambda: client.get_all_weld_details_by_work_order(""),
        },
        {
            "name": "Material Assets by Weld Serial Number",
            "function": lambda: client.get_material_assets_by_weld_serial_number("FW939"),
        },
        {
            "name": "Joiners by Weld Serial Number",
            "function": lambda: client.get_joiners_by_weld_serial_number("FW939"),
        },
        {
            "name": "Visual Inspection Results",
            "function": lambda: client.get_visual_inspection_results_by_weld_serial_number("FW939"),
        },
        {
            "name": "Weld Details by Serial Number",
            "function": lambda: client.get_weld_details_by_weld_serial_number("FW939"),
        },
        {
            "name": "NDE and CRI Inspection Details",
            "function": lambda: client.get_nde_and_cri_inspection_details("100139423P2", "250585"),
        },
        {
            "name": "MTR Metadata",
            "function": lambda: client.get_mtr_metadata("10045", "803KTEST001"),
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print("-" * 40)
        
        try:
            result = test_case['function']()
            results[test_case['name']] = result
            
            if result.get('success'):
                print("✅ Success!")
                if isinstance(result.get('data'), dict):
                    print(f"📊 Response keys: {list(result['data'].keys())}")
                print(f"🔢 Status Code: {result.get('status_code', 'Unknown')}")
            else:
                print("❌ Failed!")
                print(f"❗ Error: {result.get('error', 'Unknown error')}")
                if 'status_code' in result:
                    print(f"🔢 Status Code: {result['status_code']}")
                    
        except Exception as e:
            print(f"💥 Exception: {str(e)}")
            results[test_case['name']] = {"success": False, "error": str(e)}
    
    print("\n" + "=" * 60)
    print("📈 SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results.values() if r.get('success'))
    total = len(results)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful > 0:
        print("\n🎉 Working APIs:")
        for name, result in results.items():
            if result.get('success'):
                print(f"  • {name}")
    
    if total - successful > 0:
        print("\n⚠️ Failed APIs:")
        for name, result in results.items():
            if not result.get('success'):
                print(f"  • {name}: {result.get('error', 'Unknown error')}")
    
    return results

if __name__ == "__main__":
    print("⚠️ Please ensure the .env file is configured correctly before running tests!")
    asyncio.run(test_all_apis())