# Supervisor Agent for GasOps Weld Management System
# Intelligent query routing system that determines appropriate specialized agent based on query content

from agents.mtr_agent import handle_mtr_agent
from agents.weldInsight_agent import handle_weldinsight_agent
from config.azure_client import get_azure_chat_openai 
from prompts.supervisor_prompt import get_supervisor_prompt

# Date/time context is now handled within supervisor_prompt.py

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

    # Initialize Azure OpenAI client for query classification
    azure_client, azureopenai = get_azure_chat_openai()

    # Get comprehensive classification prompt from supervisor_prompt.py
    # This consolidates all routing logic in a single, maintainable location
    prompt = get_supervisor_prompt(query)
    # Send classification prompt to Azure OpenAI for intelligent routing decision
    response = azure_client.chat.completions.create(
        model=azureopenai,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip()

    # Parse the AI classification response into actionable routing decision
    import json
    try:
        parsed = json.loads(result)
    except Exception:
        # Fallback: treat unparseable response as direct answer
        parsed = {"answer": result}

    # Execute routing decision - delegate to specialized agent or return direct answer
    if parsed.get("agent") == "MTRAgent":
        # Route to MTR Agent for material analysis and document processing
        return handle_mtr_agent(query, auth_token)
    elif parsed.get("agent") == "WeldInsightAgent":
        # Route to WeldInsight Agent for welding operations and work orders
        return handle_weldinsight_agent(query, auth_token)
    else:
        # Handle general questions directly without agent routing
        return parsed