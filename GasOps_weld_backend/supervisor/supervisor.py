from agents.mtr_agent import handle_mtr_agent
from agents.weldinsights import handle_weldinsights
from config.azure_client import get_azure_chat_openai
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
now = datetime.now()
current_date = now.strftime('%B %d, %Y')
current_year = now.year

async def supervisor(query, database_name=None, auth_token=None):
    """
    Supervisor agent that routes queries to specialized agents based on intent analysis.

    Args:
        query (str): User's query to be processed
        database_name (str, optional): Database identifier for context
        auth_token (str, optional): Authentication token for API calls

    Returns:
        dict or str: Response from the appropriate agent or direct answer
    """
    logger.info(f"Supervisor received query for routing - database: {database_name[:10] if database_name else 'None'}...")

    try:
        azure_client, azureopenai = get_azure_chat_openai()
        logger.info("Azure OpenAI client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
        return {"error": "Service initialization failed"}

    # Use LLM prompt for all intent detection and response
    prompt = (
        f"""
        You are a supervisor managing a team of specialized agents. Your job is to understand the user's intent from their question and respond appropriately.

        User question: {query}

        Context:
        - Today's date is {current_date}, current year is {current_year}, and the time is {time}.
        - Always greet the user if they greet you. Do not give previous context in responses to greetings.
        - If the user asks a general question (e.g., about today's date, time, year, weather, day, month), answer directly and do not invoke any agent.
        - For weather questions, if you do not have real-time data, provide an approximate.
        - If the user's question is a follow-up (short or ambiguous) to a previous domain-specific question, route it to the same agent as before unless the intent clearly changes.

        Available agents and their domains:
        1. WeldInsightsAgent: Handles queries related to work orders
        2. MTRAgent: Handles queries related to material test reports, heat numbers, material properties

        Rules :
        - You do NOT answer domain-specific queries yourself. Instead, you:
        - Interpret the user's query.
        - Decide which subagent(s) should handle it.
        - Route the query to the correct subagent(s) based on scope, domain, and context.
        - Maintain strict boundaries: only return general answers if the query is outside agent scope (e.g., greetings, date, time, weather).
        - If the query is ambiguous, ask for clarification before routing.
        - If the question is a follow-up to a previous agent interaction, and the intent is unclear, prefer routing to the previous agent.

        Examples:
        User: "Show me work orders in the area of Bronx"
        Response: {{"agent": "WeldInsightsAgent"}}

        User: "Get me MTR data for heat number 12345"
        Response: {{"agent": "MTRAgent"}}

        Respond in the following format:
        - If general question: {{"answer": "<direct answer>"}}
        - If agent required: {{"agent": "<agent name>"}}
        - If user question is ambiguous: {{"answer": "<ask for clarification clearly>"}}
        """
    )
    try:
        response = azure_client.chat.completions.create(
            model=azureopenai,
            messages=[{"role": "user", "content": prompt}],
            temperature = 0.2
        )
        result = response.choices[0].message.content.strip()
        logger.info("LLM routing decision completed successfully")
    except Exception as e:
        logger.error(f"LLM routing failed: {str(e)}")
        return {"error": "Query routing failed"}

    # Try to parse the LLM response
    try:
        parsed = json.loads(result)
        logger.info(f"Successfully parsed LLM response with keys: {list(parsed.keys())}")
    except Exception as e:
        logger.warning(f"Failed to parse LLM response as JSON: {str(e)}")
        parsed = {"answer": result}

    if parsed.get("agent") == "WeldInsightsAgent":
        logger.info("Routing query to WeldInsights agent")
        try:
            return handle_weldinsights(query, auth_token)
        except Exception as e:
            logger.error(f"WeldInsights agent failed: {str(e)}")
            return {"error": "WeldInsights processing failed"}
    elif parsed.get("agent") == "MTRAgent":
        logger.info("Routing query to MTR agent")
        try:
            return handle_mtr_agent(query, auth_token)
        except Exception as e:
            logger.error(f"MTR agent failed: {str(e)}")
            return {"error": "MTR processing failed"}

    logger.info("Returning direct response (no agent routing required)")
    return parsed