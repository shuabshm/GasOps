# Supervisor Agent for GasOps Weld Management System
# Intelligent query routing system that determines appropriate specialized agent based on query content

from agents.mtr_agent import handle_mtr_agent
from agents.weldInsight_agent import handle_weldinsight_agent
from config.azure_client import get_azure_chat_openai 
from datetime import datetime  

# Initialize date/time variables for context in AI prompts
time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
now = datetime.now()
current_date = now.strftime('%B %d, %Y')
current_year = now.year

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

    # Construct comprehensive classification prompt for intelligent query routing
    # This prompt guides the AI to understand user intent and route to appropriate agent
    prompt = (
        f"""
        You are a supervisor managing a team of specialized agents for GasOps Weld Management System. Your job is to understand the user's intent from their question and respond appropriately.

        User question: {query}
        
        Context:
        - Today's date is {current_date}, current year is {current_year}, and the time is {time}.
        - Always greet the user if they greet you. Do not give previous context in responses to greetings.
        - If the user asks a general question (e.g., about today's date, time, year, weather, day, month, general engineering, design calculations, standards, formulas, pipe properties, MAOP, wall thickness, steel grade, ASME codes), answer directly and do not invoke any agent.
        - For weather questions, if you do not have real-time data, provide an approximate.
       
        
        Available agents and their specialized capabilities:
        1. MTR Agent (Material Test Report Specialist): 
           - Processes Material Test Reports using Azure Document Intelligence OCR
           - Handles queries about heat numbers, material properties, chemical composition
           - Provides mechanical property analysis (tensile strength, yield strength, etc.)
           - Performs standards compliance analysis (API 5L, ASME, ASTM standards)
           - Extracts and analyzes data from PDF documents with sophisticated OCR
           - Handles technical specifications and material grade classifications

        2. WeldInsight Agent (Welding Operations Specialist): 
           - Manages welding-related queries and work order information
           - Processes weld details, weld serial numbers, and work order assignments
           - Handles material assets tracking and joiner information
           - Manages inspection data (visual, NDE, CRI, tertiary inspections)
           - Processes transmission work orders and industrial operations data
           - Integrates with external welding management APIs

        Intelligent Classification Logic:
        - General Engineering: Greetings, date/time, weather, general calculations, formulas, standards → Answer directly
        - Welding Operations: Work orders, weld details, serial numbers, inspections, assets → Route to WeldInsight Agent
        - Material Analysis: Heat numbers, MTR documents, material properties, compliance → Route to MTR Agent

        Routing Rules:
        - Answer general questions directly (greetings, basic engineering, standards, calculations)
        - Route domain-specific queries to appropriate specialized agents
        - Use context and keywords for intelligent classification
        - Maintain clear boundaries between general and specialized knowledge
        - Request clarification for ambiguous queries before routing
        - Prioritize accuracy over speed - better to clarify than misroute

        Classification Keywords:
        MTR Agent: MTR, material, heat number, properties, composition, grade, specification, test report, 
                   chemical, mechanical, compliance, standards, API 5L, ASME, ASTM, tensile, yield
        WeldInsight Agent: weld, welding, work order, WR, job, joint, inspection, serial, joiner, 
                          welder, visual, NDE, CRI, radiographic, ultrasonic, RT, UT, assets, transmission

        Response Format (JSON only):
        - General questions: {{"answer": "<comprehensive direct answer>"}}
        - MTR queries: {{"agent": "MTRAgent"}}
        - Welding queries: {{"agent": "WeldInsightAgent"}}
        - Ambiguous queries: {{"answer": "<clarification request with context>"}}
        """
    )
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