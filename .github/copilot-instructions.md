# GitHub Copilot Instructions

## Project Overview
GasOps Weld Backend is a FastAPI-based backend service for weld management. It uses AI agents to process weld-related queries, integrating with Azure OpenAI and Azure Document Intelligence.

## Key Technologies
- Python 3.12.5
- FastAPI with async support
- Azure OpenAI
- Azure Document Intelligence (OCR)
- Pydantic for data validation

## Code Conventions
- Use async/await for all I/O-bound operations
- Use Pydantic models for request and response validation
- Follow existing agent patterns in the `agents/` directory
- Use structured logging via the `logging` module
- Document all new functions and classes with docstrings

## Architecture Notes
- `supervisor/supervisor.py`: Routes queries to the appropriate agent
- `agents/mtr_agent.py`: Handles Material Test Report processing
- `agents/weldinsights.py`: Handles WeldInsights API integration
- `tools/`: Contains utility functions for API calls and data processing
- `config/`: Azure client setup and credential decryption

## Environment Variables
Required `.env` variables include Azure OpenAI credentials, Azure Document Intelligence credentials, and authentication tokens. Never commit secrets or credentials.
