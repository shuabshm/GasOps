# GasOps Weld Backend

## Project Overview
A FastAPI-based backend service for the GasOps Weld Management System that provides RESTful endpoints for processing weld-related queries using AI agents. The system uses intelligent routing to direct queries to specialized agents for Material Test Reports (MTR) and WeldInsights analysis.

## System Requirements
- Python version: 3.12.5

## Key Features
- Token-based authentication with encrypted credentials
- Session management for multi-turn conversations
- AI-powered query routing to specialized agents (MTR and WeldInsights)
- Integration with Azure OpenAI for intelligent query processing
- Azure Document Intelligence OCR for PDF processing
- Comprehensive error handling and robust logging
- Certificate-based external API authentication
- Intelligent conversation context handling

## Architecture
- FastAPI web framework with async support
- Supervisor agent for intelligent query routing
- Specialized agents for domain-specific processing
- Azure services integration (OpenAI, Document Intelligence)
- Advanced OCR capabilities for Material Test Reports

## Directory Structure
```
GasOps_weld_backend/
├── agents/                     # AI agent implementations
│   ├── mtr_agent.py           # MTR-specific processing agent with OCR
│   └── weldinsights.py        # WeldInsights API integration agent
├── certificate/               # SSL certificates for external API calls
├── config/                    # Configuration and authentication
│   ├── azure_client.py        # Azure service client setup
│   └── decryption.py         # Credential decryption utilities
├── prompts/                   # AI prompt templates
│   ├── mtr_prompt.py         # MTR agent prompts
│   ├── data_analysis_prompt.py # Data analysis prompts
│   └── weld_api_router_prompt.py # API routing prompts
├── supervisor/                # Query routing logic
│   └── supervisor.py         # Main supervisor implementation
├── tools/                     # Utility functions and API clients
│   ├── execute_api.py        # Generic API execution utility
│   ├── mtr_tools.py          # MTR processing tools
│   └── weldinsights_tools.py # WeldInsights processing tools
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
3. Configure environment variables in .env file:
   - Azure OpenAI credentials
   - Azure Document Intelligence credentials
   - Authentication tokens
4. Run application: `uvicorn main:app --reload`

## API Endpoints
- POST /ask - Main endpoint for processing weld-related queries
- Supports token-based authentication via encoded_string header
- Returns JSON responses with processed query results
- Session management for multi-turn conversations

## Agent Capabilities
### MTR Agent
- Material Test Report processing with OCR
- Heat number queries and material properties analysis
- Standards compliance validation (API 5L, ASME, etc.)
- Chemical composition and mechanical properties analysis

### WeldInsights Agent
- Work order management and queries
- Weld data analysis and reporting
- Integration with external weld management APIs
