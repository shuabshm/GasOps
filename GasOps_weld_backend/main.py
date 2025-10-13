from fastapi import FastAPI, Header, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from config.decryption import decode, generate_auth_token
from supervisor.supervisor import supervisor
from datetime import datetime, timezone, timedelta
import json
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gasops_weld.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with metadata
app = FastAPI(title="GasOps Weld Backend", version="1.0.0")
logger.info("FastAPI application initialized")
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

# In-memory session storage for development
# TODO: Replace with Redis or similar distributed cache in production
active_sessions = {}

logger.info("GasOps Weld Backend initialized successfully")

@app.post("/ask")
async def ask(
    body: AskRequest = Body(...),
    encoded_string: str = Header(...)
):
    # Log request details with session masking for security
    session_masked = f"***{body.session_id[-4:]}" if body.session_id and len(body.session_id) > 4 else "None"
    logger.info(f"Processing query request for session: {session_masked}")
    query = body.query
    prev_msgs = body.prev_msgs or []
    session_id = body.session_id

    # Build conversation context from recent messages to maintain context awareness
    # Limit to last 3 messages to prevent token limit issues while preserving recent context
    last_msgs = prev_msgs[-3:]
    context = "\\n".join([f"Previous message {i+1} ({msg.role}): {msg.content}" for i, msg in enumerate(last_msgs)])
    full_question = f"{context}\\nCurrent question: {query}" if context else query
    logger.info(f"Full question: {full_question}")
    logger.info(f"Processing query with context length: {len(context) if context else 0} characters")

    # Initialize variables for credential extraction and token processing
    database_name = None  # Extracted from decoded token
    decrypted_fields = {}  # Decoded organization credentials
    auth_token = None  # Generated token for external API calls

    if encoded_string:
        try:
            decrypted_fields = decode(encoded_string)
            org_id_masked = f"***{decrypted_fields.get('OrgID', 'unknown')[-4:]}" if decrypted_fields.get('OrgID') and len(decrypted_fields.get('OrgID', '')) > 4 else "unknown"
            logger.info(f"Successfully decoded credentials for org: {org_id_masked}")
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
                logger.info(f"Session cached for ID: {session_masked}")
        except Exception as e:
            logger.error(f"Failed to decode token: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid token")

    if not auth_token:
        logger.warning("Authentication token missing in request")
        raise HTTPException(status_code=400, detail="Auth token required")

    try:
        result = await supervisor(full_question, database_name, auth_token)
        success = isinstance(result, dict) and not result.get('error')
        logger.info(f"Supervisor agent completed processing - success: {success}")
    except Exception as e:
        logger.error(f"Supervisor processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing error")

    # Extract the main response text, always as a string
    response_text = None
    if isinstance(result, dict):
        if "answer" in result:
            response_text = result["answer"]
            while isinstance(response_text, dict) and "answer" in response_text:
                response_text = response_text["answer"]
        elif "error" in result:
            response_text = "Server is down, please try again in some time."
        else:
            response_text = str(result)
    else:
        response_text = str(result)

    if not isinstance(response_text, str):
        response_text = json.dumps(response_text, ensure_ascii=False)

    timestamp_bot = datetime.utcnow().isoformat()
    context_list = [
        {"role": "user", "content": query, "timestamp": timestamp_bot},
        {"role": "assistant", "content": response_text, "timestamp": timestamp_bot}
    ]

    # User details
    user_details = {
        "session_id": session_id,
        "token": body.token
    }

    # Handle specs sources if available
    sources = []
    if isinstance(result, dict) and "sources" in result:
        sources = result["sources"]
        logger.info(f"Included {len(sources)} spec sources in response")

    # 6-field response format with sources support
    return {
        "answer": response_text,
        "timestamp": timestamp_bot,
        "context": context_list,
        "user_details": user_details,
        "decrypted_fields": decrypted_fields,
        "sources": sources  # Include specs sources for citations
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)