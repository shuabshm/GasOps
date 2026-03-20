# GasOps Copilot Instructions

## Project Overview
GasOps Weld Backend is a FastAPI-based backend service for the GasOps Weld Management System. It provides RESTful endpoints for processing weld-related queries using AI agents powered by Azure OpenAI.

## Tech Stack
- **Language**: Python 3.12.5
- **Framework**: FastAPI with async support
- **AI Services**: Azure OpenAI, Azure Document Intelligence
- **Authentication**: Token-based with encrypted credentials

## Architecture
- `main.py` — FastAPI application entry point with `/ask` endpoint
- `supervisor/supervisor.py` — Routes queries to appropriate specialist agents
- `agents/mtr_agent.py` — Processes Material Test Reports (MTR) with OCR
- `agents/weldinsights.py` — Integrates with WeldInsights API for work order and weld data
- `agents/specs_agent.py` — Handles specification-related queries
- `config/` — Azure client setup and credential decryption
- `tools/` — API execution utilities and domain-specific tools
- `utils/` — Data transformation and extraction helpers
- `prompts/` — AI prompt templates for each agent

## Coding Conventions
- Use `async`/`await` for all route handlers and agent calls
- Follow FastAPI patterns for dependency injection and request validation
- Use Pydantic models for request/response schemas
- Log significant operations using the `logger` from the `logging` module
- Handle errors with `HTTPException` and appropriate status codes

## Key Domain Concepts
- **MTR (Material Test Report)**: Documents certifying material properties (chemical composition, mechanical properties) per standards like API 5L, ASME
- **WeldInsights**: External API providing work order management and weld data analysis
- **Supervisor Agent**: Intelligently routes user queries to MTR or WeldInsights agents based on query content
