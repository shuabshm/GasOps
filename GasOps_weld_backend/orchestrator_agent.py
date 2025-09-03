from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class OrchestratorAgent:
    def __init__(self):
        self.azure_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        )
    
    async def process(self, query, auth_token):
        # Just pass everything to database agent
        from database_agent import DatabaseAgent
        db_agent = DatabaseAgent()
        return await db_agent.process(query, auth_token)

