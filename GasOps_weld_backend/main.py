"""
GasOps Weld Backend API

A FastAPI-based backend service for the GasOps Weld Management System.
Provides RESTful endpoints for processing weld-related queries using AI agents.

Key Features:
- Token-based authentication with encrypted credentials
- Session management for multi-turn conversations
- AI-powered query routing to specialized agents (MTR and WeldInsight)
- Integration with Azure OpenAI for intelligent query processing
- Comprehensive error handling and logging

Architecture:
- FastAPI web framework with async support
- Supervisor agent for intelligent query routing
- Specialized agents for domain-specific processing
- Azure services integration (OpenAI, Document Intelligence)
- Certificate-based external API authentication
"""
from fastapi import FastAPI, Header, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel
from typing import List, Optional
from config.decryption import decode, generate_auth_token
from supervisor.supervisor import supervisor
from datetime import datetime, timezone, timedelta
import json

# Configure logging to suppress verbose Azure/HTTP logs while maintaining INFO level for app logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with metadata
app = FastAPI(title="GasOps Weld Backend", version="1.0.0")

# Configure CORS middleware to allow cross-origin requests from frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation and serialization

class Message(BaseModel):
    """Represents a conversation message with role and content"""
    role: str  # 'user' or 'assistant'
    content: str

class AskRequest(BaseModel):
    """Request model for the main query endpoint"""
    query: str  # User's question or request
    prev_msgs: Optional[List[Message]] = None  # Conversation history for context
    token: Optional[str] = None  # Legacy token field (optional)
    session_id: Optional[str] = None  # Session identifier for multi-turn conversations

class AuthRequest(BaseModel):
    """Request model for token generation endpoint"""
    orgID: str  # Organization identifier
    databasename: str  # Database name for the organization
    masterID: str  # Master login identifier

# In-memory session storage for development
# TODO: Replace with Redis or similar distributed cache in production
active_sessions = {}

logger.info("GasOps Weld Backend initialized successfully")

@app.get("/")
async def root():
    """Root endpoint for health check and API identification"""
    return {"message": "GasOps Weld Backend API is running"}

@app.post("/generate-token")
async def generate_token(auth_request: AuthRequest):
    """
    Generate authentication token from organization credentials.
    
    This endpoint creates a base64-encoded token containing organization details
    and timestamps for API authentication. The token is valid for 24 hours.
    
    Args:
        auth_request: Contains orgID, databasename, and masterID
    
    Returns:
        dict: Contains success status, token, and expiration info
    
    Raises:
        HTTPException: If token generation fails
    """
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
    """
    Main query processing endpoint for the GasOps Weld System.
    
    Processes user queries through intelligent agent routing system.
    Supports conversation context, session management, and token-based authentication.
    
    Args:
        body: Request containing query, previous messages, and session info
        encoded_string: Base64-encoded authentication credentials (Header)
    
    Returns:
        dict: Standardized response with answer, timestamp, context, 
              user_details, and decrypted_fields
              
    Raises:
        HTTPException: For authentication failures or invalid tokens
        
    Flow:
        1. Extract conversation context from previous messages
        2. Decode and validate authentication token
        3. Generate API authentication token
        4. Route query through supervisor agent
        5. Format and return standardized response
    """
    # Log request for debugging (remove in production for security)
    logger.debug(f"Processing query request for session: {body.session_id}")
    query = body.query
    prev_msgs = body.prev_msgs or []
    session_id = body.session_id
    
    # Build conversation context from recent messages to maintain context awareness
    # Limit to last 3 messages to prevent token limit issues while preserving recent context
    last_msgs = prev_msgs[-3:]
    context = "\\n".join([f"Previous message {i+1} ({msg.role}): {msg.content}" for i, msg in enumerate(last_msgs)])
    full_question = f"{context}\\nCurrent question: {query}" if context else query
    logger.info(f"Processing query with context length: {len(context) if context else 0} characters")

    # Initialize variables for credential extraction and token processing
    database_name = None  # Extracted from decoded token
    decrypted_fields = {}  # Decoded organization credentials
    auth_token = None  # Generated token for external API calls
    
    if encoded_string:
        try:
            decrypted_fields = decode(encoded_string)
            logger.info(f"Successfully decoded credentials for org: {decrypted_fields.get('OrgID', 'unknown')}")
            database_name = decrypted_fields.get("Database_Name")
            
            # Generate authentication token for external API calls using decoded credentials
            # This token follows a specific format required by the weld management system APIs
            auth_token = generate_auth_token(
                decrypted_fields.get('LoginMasterID'),
                decrypted_fields.get('Database_Name'), 
                decrypted_fields.get('OrgID')
            )
            logger.info("Generated authentication token for API calls")
            
            # Cache session information for improved performance in multi-turn conversations
            # Stores credentials and tokens to avoid re-decoding on subsequent requests
            if session_id:
                active_sessions[session_id] = {
                    "credentials": decrypted_fields,
                    "auth_token": auth_token,
                    "last_access": datetime.now(timezone.utc)  # Track for session cleanup
                }
                
        except Exception as e:
            logger.error(f"Failed to decode token: {e}")
            raise HTTPException(status_code=400, detail="Invalid token")

    if not auth_token:
        raise HTTPException(status_code=400, detail="Auth token required")

    try:
        # Route query to supervisor agent for intelligent processing
        # Supervisor determines appropriate specialized agent (MTR or WeldInsight) based on query content
        result = await supervisor(full_question, database_name, auth_token)
        logger.info(f"Supervisor agent completed processing - success: {isinstance(result, dict) and not result.get('error')}")
        
        # Extract and normalize response content from supervisor agent result
        # Handle various response formats from different agents and processing paths
        response_text = None
        if isinstance(result, dict):
            if "data" in result:
                response_text = result["data"]
            elif "answer" in result:
                response_text = result["answer"]
                # Handle nested answer structure
                while isinstance(response_text, dict) and "answer" in response_text:
                    response_text = response_text["answer"]
            elif "error" in result:
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

        # 5-field response format following OQ pattern
        return {
            "answer": response_text,
            "timestamp": timestamp_bot,
            "context": context_list,
            "user_details": user_details,
            "decrypted_fields": decrypted_fields
        }
        
    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}")
        timestamp_bot = datetime.utcnow().isoformat()
        
        # 5-field error response structure
        return {
            "answer": "Server is down, please try again in some time.",
            "timestamp": timestamp_bot,
            "context": [
                {"role": "user", "content": query, "timestamp": timestamp_bot},
                {"role": "assistant", "content": "Server error occurred", "timestamp": timestamp_bot}
            ],
            "user_details": {"session_id": session_id, "token": body.token},
            "decrypted_fields": decrypted_fields
        }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancer probes.
    
    Returns system status and basic metrics including active session count.
    Useful for deployment health monitoring and debugging.
    """
    return {
        "status": "healthy", 
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_sessions": len(active_sessions)
    }

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """
    Retrieve session information for debugging and development purposes.
    
    Returns session existence status, cached credentials, and last access time.
    Should be disabled or secured in production environments.
    
    Args:
        session_id: The session identifier to look up
        
    Returns:
        dict: Session information or existence status
    """
    if session_id in active_sessions:
        session = active_sessions[session_id]
        return {
            "exists": True,
            "credentials": session["credentials"],
            "last_access": session["last_access"].isoformat()
        }
    return {"exists": False}

# Development server configuration
# In production, use a proper ASGI server like Gunicorn with Uvicorn workers
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)