"""
FastAPI Backend for GasOps Weld System
Main entry point following centralized token management approach
"""
from fastapi import FastAPI, Header, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel
from typing import List, Optional
from token_utils import decode_token, generate_auth_token
from supervisor_agent import SupervisorAgent
from datetime import datetime, timezone, timedelta
import json

# Setup logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GasOps Weld Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://0.0.0.0:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class AskRequest(BaseModel):
    query: str
    prev_msgs: Optional[List[Message]] = None
    token: Optional[str] = None
    session_id: Optional[str] = None

class AuthRequest(BaseModel):
    orgID: str
    databasename: str
    masterID: str

# Session storage (in production, use Redis or similar)
active_sessions = {}

print("Main module loaded successfully.")

@app.get("/")
async def root():
    return {"message": "GasOps Weld Backend API is running"}

@app.post("/generate-token")
async def generate_token(auth_request: AuthRequest):
    """Generate authentication token from frontend credentials"""
    try:
        token = generate_auth_token(
            auth_request.masterID,
            auth_request.databasename, 
            auth_request.orgID
        )
        return {
            "success": True,
            "token": token,
            "expires_in": "24 hours"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token generation failed: {str(e)}")

@app.post("/ask")
async def ask(
    body: AskRequest = Body(...),
    encoded_string: str = Header(...)
):
    """Process user query with centralized token management"""
    print(f"Received request body: {body}")
    query = body.query
    prev_msgs = body.prev_msgs or []
    session_id = body.session_id
    
    # Build context from previous messages
    last_msgs = prev_msgs[-3:]
    context = "\n".join([f"Previous message {i+1} ({msg.role}): {msg.content}" for i, msg in enumerate(last_msgs)])
    full_question = f"{context}\nCurrent question: {query}" if context else query
    print(f"Full question: {full_question}")
    logger.info(f"Full question: {full_question}")

    # Decode token and extract credentials
    database_name = None
    decrypted_fields = {}
    auth_token = None
    
    if encoded_string:
        try:
            decrypted_fields = decode_token(encoded_string)
            print(f"Decrypted token: {decrypted_fields}")
            database_name = decrypted_fields.get("Database_Name")
            
            # Generate auth token for API calls
            auth_token = generate_auth_token(
                decrypted_fields.get('LoginMasterID'),
                decrypted_fields.get('Database_Name'), 
                decrypted_fields.get('OrgID')
            )
            print(f"Generated auth_token: {auth_token}")
            
            # Store session info if session_id provided
            if session_id:
                active_sessions[session_id] = {
                    "credentials": decrypted_fields,
                    "auth_token": auth_token,
                    "last_access": datetime.now(timezone.utc)
                }
                
        except Exception as e:
            logger.error(f"Failed to decode token: {e}")
            raise HTTPException(status_code=400, detail="Invalid token")

    if not auth_token:
        raise HTTPException(status_code=400, detail="Auth token required")

    try:
        # Process query using supervisor agent
        supervisor = SupervisorAgent()
        result = await supervisor.process(full_question, auth_token)
        print(f"Supervisor agent result: {result}")
        
        # Extract response text
        response_text = None
        if isinstance(result, dict):
            if "data" in result:
                response_text = result["data"]
            elif "error" in result:
                # Use the actual error message from the agent instead of generic message
                response_text = result["error"]
            else:
                response_text = str(result)
        else:
            response_text = str(result)

        # If response_text is not a string, serialize to JSON
        if not isinstance(response_text, str):
            response_text = json.dumps(response_text, ensure_ascii=False)

        # Build response context
        timestamp_bot = datetime.utcnow().isoformat()
        context_list = [
            {
                "role": "user",
                "content": query,
                "timestamp": timestamp_bot
            },
            {
                "role": "assistant", 
                "content": response_text,
                "timestamp": timestamp_bot
            }
        ]

        # User details
        user_details = {
            "session_id": session_id,
            "token": body.token
        }

        # SQL queries if available
        sql_queries = []
        if isinstance(result, dict) and result.get("data"):
            sql_queries.append({
                "db": database_name or "",
                "query": "API call executed"
            })

        # Sources if available
        sources = []
        if isinstance(result, dict) and "sources" in result:
            sources = result["sources"]

        # Extract APIs called from agent response
        apis_called = []
        if isinstance(result, dict):
            # Get APIs from agent response or default to supervisor for general queries
            if "apis_called" in result:
                apis_called = result["apis_called"]
            elif result.get("agent") == "supervisor agent":
                apis_called = ["/supervisor"]
            elif result.get("agent") == "weldInsight agent" and result.get("success"):
                # Extract API info from weldInsight agent if available
                apis_called = ["/openai/chat/completions"]  # At minimum it uses OpenAI for classification
            
        # return {
        #     "answer": response_text,
        #     "timestamp": timestamp_bot,
        #     "context": context_list,
        #     "user_details": user_details, 
        #     "sql_queries": sql_queries,
        #     "sources": sources,
        #     "decrypted_fields": decrypted_fields,
        #     "success": result.get("success", True),
        #     "agent": result.get("agent"),
        #     "ai_classification": result.get("ai_classification")
        # }
        
        #return structure
        return {
            "answer": response_text,
            "timestamp": timestamp_bot,
            "context": context_list,
            "user_details": user_details,
            "Apis": apis_called,
            "decrypted_fields": decrypted_fields
        }
        
    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}")
        timestamp_bot = datetime.utcnow().isoformat()
        
        # return {
        #     "answer": "Server is down, please try again in some time.",
        #     "timestamp": timestamp_bot,
        #     "context": [
        #         {"role": "user", "content": query, "timestamp": timestamp_bot},
        #         {"role": "assistant", "content": "Server error occurred", "timestamp": timestamp_bot}
        #     ],
        #     "user_details": {"session_id": session_id, "token": body.token},
        #     "sql_queries": [],
        #     "sources": [],
        #     "decrypted_fields": decrypted_fields,
        #     "success": False,
        #     "agent": "unknown"
        # }
        
        # 6-field error return structure
        return {
            "answer": "Server is down, please try again in some time.",
            "timestamp": timestamp_bot,
            "context": [
                {"role": "user", "content": query, "timestamp": timestamp_bot},
                {"role": "assistant", "content": "Server error occurred", "timestamp": timestamp_bot}
            ],
            "user_details": {"session_id": session_id, "token": body.token},
            "Apis": [],
            "decrypted_fields": decrypted_fields
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_sessions": len(active_sessions)
    }

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Get session information for debugging"""
    if session_id in active_sessions:
        session = active_sessions[session_id]
        return {
            "exists": True,
            "credentials": session["credentials"],
            "last_access": session["last_access"].isoformat()
        }
    return {"exists": False}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)