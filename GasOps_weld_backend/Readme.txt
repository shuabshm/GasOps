# GasOps Weld Backend

## Project Overview
A FastAPI-based backend service for the GasOps Weld Management System that provides RESTful endpoints for processing weld-related queries using AI agents.

## System Requirements
- Python version: 3.12.5

## Key Features
- Token-based authentication with encrypted credentials
- Session management for multi-turn conversations
- AI-powered query routing to specialized agents (MTR and WeldInsight)
- Integration with Azure OpenAI for intelligent query processing
- Comprehensive error handling and logging
- Certificate-based external API authentication

## Architecture
- FastAPI web framework with async support
- Supervisor agent for intelligent query routing
- Specialized agents for domain-specific processing
- Azure services integration (OpenAI, Document Intelligence)

## Directory Structure
```
GasOps_weld_backend/
├── agents/                     # AI agent implementations
│   ├── mtr_agent.py           # MTR-specific processing agent
│   └── weldInsight_agent.py   # WeldInsight API integration agent
├── certificate/               # SSL certificates for external API calls
├── config/                    # Configuration and authentication
│   ├── azure_client.py        # Azure service client setup
│   └── decryption.py         # Credential decryption utilities
├── prompts/                   # AI prompt templates
│   ├── mtr_prompt.py         # MTR agent prompts
│   ├── supervisor_prompt.py   # Supervisor routing prompts
│   └── weldinsight_prompt.py  # WeldInsight agent prompts
├── supervisor/                # Query routing logic
│   └── supervisor.py         # Main supervisor implementation
├── tools/                     # Utility functions and API clients
│   ├── calling_api_weld.py   # WeldInsight API client
│   ├── mtr_tools.py          # MTR processing tools
│   └── weldinsight_tools.py  # WeldInsight processing tools
├── utils/                     # General utilities
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
└── .env                      # Environment variables

## Dependencies
- fastapi==0.116.1
- uvicorn==0.35.0
- requests==2.32.5
- requests-pkcs12==1.24
- pydantic==2.11.7
- python-multipart==0.0.12
- python-dotenv==1.0.0
- azure-ai-documentintelligence==1.0.0
- azure-core==1.30.2
- openai==1.104.2

## Installation & Setup
1. Install Python 3.12.5
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in .env file
4. Run application: `uvicorn main:app --reload`

## API Endpoints
- POST /weld_question - Main endpoint for processing weld-related queries
- Supports token-based authentication via Authorization header
- Returns JSON responses with processed query results
