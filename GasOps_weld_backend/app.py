"""
FastAPI Backend for GasOps Weld System
Handles frontend connection and auth token generation
"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from datetime import datetime, timezone, timedelta
from typing import Optional
import asyncio
from orchestrator_agent import OrchestratorAgent
from api_client import APIClient

app = FastAPI(title="GasOps Weld Backend", version="1.0.0")

# CORS configuration for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://0.0.0.0:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthRequest(BaseModel):
    orgID: str
    databasename: str
    masterID: str

class QueryRequest(BaseModel):
    query: str
    token: str
    session_id: Optional[str] = None
    prev_msgs: Optional[list] = None

def generate_auth_token(org_id: str, database_name: str, master_id: str) -> str:
    """Generate auth token from provided credentials"""
    now_utc = datetime.now(timezone.utc)
    date_plus_one = (now_utc + timedelta(days=1)).isoformat()
    date_now = now_utc.isoformat()
    
    token_str = f"{date_plus_one}&{master_id}&{database_name}&{date_now}&{org_id}"
    return base64.b64encode(token_str.encode('utf-8')).decode('utf-8')

@app.get("/")
async def root():
    return {"message": "GasOps Weld Backend API is running"}

@app.post("/generate-token")
async def generate_token(auth_request: AuthRequest):
    """Generate authentication token from frontend credentials"""
    try:
        token = generate_auth_token(
            auth_request.orgID,
            auth_request.databasename,
            auth_request.masterID
        )
        return {
            "success": True,
            "token": token,
            "expires_in": "24 hours"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token generation failed: {str(e)}")

@app.post("/ask")
async def process_query(query_request: QueryRequest, encoded_string: str = Header(None)):
    """Process user query with original frontend format"""
    try:
        # Use the token from either the request body or header (frontend sends both)
        auth_token = query_request.token or encoded_string
        
        if not auth_token:
            raise HTTPException(status_code=400, detail="Auth token required")
        
        # Create orchestrator and process query
        orchestrator = OrchestratorAgent()
        result = await orchestrator.process(query_request.query, auth_token)
        
        return {
            "success": result.get("success", False),
            "data": result.get("data"),
            "error": result.get("error"),
            "agent": result.get("agent"),
            "ai_classification": result.get("ai_classification")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)