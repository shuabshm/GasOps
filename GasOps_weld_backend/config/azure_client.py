# Azure OpenAI Client Configuration
# Centralized configuration for Azure OpenAI services integration
# Handles authentication, endpoint management, and client initialization

import openai
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file if present
import os

# Azure OpenAI service configuration from environment variables
# These values should be set in .env file or environment for security
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # Model deployment name
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")  # Underlying model (e.g., gpt-4)
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")  # API version (e.g., 2024-02-15-preview)

# Initialize Azure OpenAI client using OpenAI SDK v1+ format
# This client is used across all agents for AI-powered query processing
azure_client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

def get_azure_chat_openai():
    """
    Provide Azure OpenAI client and deployment configuration for agents.
    
    This function serves as the main entry point for agents to access
    Azure OpenAI services with consistent configuration.
    
    Returns:
        tuple: (azure_client, deployment_name) for use in chat completions
        
    Usage:
        azure_client, deployment = get_azure_chat_openai()
        response = azure_client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": prompt}]
        )
    """
    return azure_client, AZURE_OPENAI_DEPLOYMENT