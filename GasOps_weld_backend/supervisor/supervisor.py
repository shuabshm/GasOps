# Supervisor Agent for GasOps Weld Management System
# Intelligent query routing system that determines appropriate specialized agent based on query content

import logging
from agents.mtr_agent import handle_mtr_agent
from agents.weldInsight_agent import handle_weldinsight_agent
from config.azure_client import get_azure_chat_openai
from prompts.supervisor_prompt import get_supervisor_prompt

# Date/time context is now handled within supervisor_prompt.py
logger = logging.getLogger(__name__)

async def supervisor(query, database_name=None, auth_token=None):
    """
    Main supervisor agent for intelligent query routing in the GasOps Weld System.

    This function acts as a smart dispatcher that analyzes user queries and routes them
    to the most appropriate specialized agent (MTR or WeldInsight) based on content analysis.
    Also handles general queries directly without agent routing.

    Architecture:
    - Uses Azure OpenAI for intelligent query classification
    - Supports general queries (greetings, engineering calculations, standards)
    - Routes domain-specific queries to specialized agents
    - Maintains conversation context and handles follow-up questions

    Args:
        query (str): User's question or request (may include conversation context)
        database_name (str, optional): Database identifier for multi-tenant support
        auth_token (str, optional): Authentication token for external API calls

    Returns:
        dict or str: Response from appropriate agent or direct answer for general queries

    Agent Routing Logic:
    - MTR Agent: Material properties, heat numbers, test reports, compliance analysis
    - WeldInsight Agent: Work orders, weld details, inspections, industrial operations
    - Direct Response: Greetings, general engineering questions, standards, calculations
    """

    logger.info(f"=== SUPERVISOR QUERY ANALYSIS ===")
    logger.info(f"Query length: {len(query)} characters")
    logger.info(f"Query content: {query}")
    logger.info(f"Auth token provided: {bool(auth_token)}")
    logger.info(f"Database name: {database_name}")

    # Initialize Azure OpenAI client for query classification
    logger.info("=== AZURE OPENAI INITIALIZATION ===")
    azure_client, azureopenai = get_azure_chat_openai()
    logger.info(f"Azure OpenAI model: {azureopenai}")

    # Get comprehensive classification prompt from supervisor_prompt.py
    # This consolidates all routing logic in a single, maintainable location
    logger.info("=== GENERATING CLASSIFICATION PROMPT ===")
    prompt = get_supervisor_prompt(query)
    logger.info(f"Prompt generated - length: {len(prompt)} characters")

    # Send classification prompt to Azure OpenAI for intelligent routing decision
    logger.info(f"=== CALLING AZURE OPENAI FOR CLASSIFICATION ===")
    response = azure_client.chat.completions.create(
        model=azureopenai,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip()
    logger.info(f"=== AZURE OPENAI CLASSIFICATION RESPONSE ===")
    logger.info(f"Response length: {len(result)} characters")
    logger.info(f"Raw response: {result}")

    # Parse the AI classification response into actionable routing decision
    import json
    logger.info(f"=== PARSING CLASSIFICATION RESPONSE ===")
    try:
        parsed = json.loads(result)
        logger.info(f"Successfully parsed JSON response")
        logger.info(f"Parsed response: {parsed}")
        logger.info(f"Agent specified: {parsed.get('agent', 'no agent specified')}")
        if 'answer' in parsed:
            logger.info(f"Direct answer provided: {parsed['answer'][:100]}...")
    except Exception as e:
        # Fallback: treat unparseable response as direct answer
        logger.warning(f"Failed to parse JSON response, treating as direct answer: {str(e)}")
        logger.warning(f"Raw response that failed to parse: {result}")
        parsed = {"answer": result}

    # Execute routing decision - delegate to specialized agent or return direct answer
    logger.info(f"=== ROUTING DECISION ===")
    agent_choice = parsed.get("agent")
    logger.info(f"Agent choice: {agent_choice}")

    if agent_choice == "MTRAgent":
        # Route to MTR Agent for material analysis and document processing
        logger.info("=== ROUTING TO MTR AGENT ===")
        try:
            result = handle_mtr_agent(query, auth_token)
            logger.info("MTR Agent processing completed successfully")
            logger.info(f"MTR Agent result type: {type(result)}")
            return result
        except Exception as e:
            logger.error(f"MTR Agent processing failed: {str(e)}")
            raise
    elif agent_choice == "WeldInsightAgent":
        # Route to WeldInsight Agent for welding operations and work orders
        logger.info("=== ROUTING TO WELDINSIGHT AGENT ===")
        try:
            result = handle_weldinsight_agent(query, auth_token)
            logger.info("WeldInsight Agent processing completed successfully")
            logger.info(f"WeldInsight Agent result type: {type(result)}")
            if isinstance(result, dict):
                logger.info(f"WeldInsight Agent result keys: {list(result.keys())}")
            return result
        except Exception as e:
            logger.error(f"WeldInsight Agent processing failed: {str(e)}")
            raise
    else:
        # Handle general questions directly without agent routing
        logger.info("=== HANDLING DIRECTLY (NO AGENT ROUTING) ===")
        logger.info(f"Direct response type: {type(parsed)}")
        logger.info(f"Direct response: {parsed}")
        return parsed