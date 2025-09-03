# main.py
import asyncio
import base64
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from orchestrator_agent import OrchestratorAgent

load_dotenv()

def generate_auth_token():
    """Generate auth token from .env variables"""
    now_utc = datetime.now(timezone.utc)
    date_plus_one = (now_utc + timedelta(days=1)).isoformat()
    date_now = now_utc.isoformat()
    
    token_str = f"{date_plus_one}&{os.getenv('AUTH_TOKEN_LOGIN_MASTER_ID')}&{os.getenv('AUTH_TOKEN_DATABASE_NAME')}&{date_now}&{os.getenv('AUTH_TOKEN_ORG_ID')}"
    return base64.b64encode(token_str.encode('utf-8')).decode('utf-8')

async def handle_user_question(query):
    """Main handler function"""
    print(f"Processing: {query}")
    
    # Generate auth token
    auth_token = generate_auth_token()
    
    # Create orchestrator and process
    orchestrator = OrchestratorAgent()
    result = await orchestrator.process(query, auth_token)
    
    return result

async def test_system():
    """Test the system"""
    test_queries = [
        "Show me work order 280489410001",
        "Get all welds for WR Number ASTP312032020", 
        "Find work orders in Manhattan",
        "Show weld details for work order 10302024"
    ]
    
    print("🧪 Testing Agent System")
    print("=" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 25)
        
        try:
            result = await handle_user_question(query)
            
            if result.get("success"):
                print("✅ SUCCESS")
                print(f"🤖 Agent: {result.get('agent')}")
                print(f"🧠 AI: {result.get('ai_classification', {}).get('type')}")
                print(f"📊 Data: {len(str(result.get('data', {})))} chars")
            else:
                print("❌ FAILED")
                print(f"❗ Error: {result.get('error')}")
                
        except Exception as e:
            print(f"💥 ERROR: {e}")
        
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(test_system())