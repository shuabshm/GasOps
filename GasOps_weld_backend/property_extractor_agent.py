"""
Property Extractor Agent for extracting specific properties, measurements, and technical specifications
"""
from langchain.schema import HumanMessage, SystemMessage
import json
from azure_client import get_azure_chat_openai

class PropertyExtractorAgent:
    def __init__(self):
        try:
            self.azure_client = get_azure_chat_openai()
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {str(e)}")
            raise e
    
    async def process(self, query, auth_token):
        """Process property extraction queries"""
        try:
            # Analyze the query to determine what properties to extract
            analysis = self._analyze_extraction_request(query)
            
            # For now, return a placeholder response since we don't have documents to extract from
            response = self._generate_extraction_response(analysis, query)
            
            return {
                "success": True,
                "data": response,
                "agent": "property_extractor_agent",
                "query_type": "property_extraction",
                "analysis": analysis
            }
            
        except Exception as e:
            return {
                "success": False, 
                "error": str(e), 
                "agent": "property_extractor_agent"
            }
    
    def _analyze_extraction_request(self, query):
        """Analyze what properties the user wants to extract"""
        analysis_prompt = f"""
Analyze this property extraction request and identify what the user wants to extract.

Query: "{query}"

Determine:
1. What type of properties are being requested (materials, dimensions, specifications, etc.)
2. What format the user might expect the results in
3. What additional information might be needed

Respond with JSON in this format:
{{
    "property_type": "materials|dimensions|specifications|technical_data|other",
    "expected_format": "table|list|detailed_report|key_value_pairs",
    "required_inputs": ["list of what might be needed like document_id, part_number, etc."],
    "confidence": 0.85
}}
"""
        
        try:
            messages = [
                SystemMessage(content="You are a property extraction analyzer. Respond only with valid JSON."),
                HumanMessage(content=analysis_prompt)
            ]
            
            response = self.azure_client.invoke(messages)
            analysis_text = response.content.strip()
            return json.loads(analysis_text)
            
        except Exception as e:
            return {
                "property_type": "other",
                "expected_format": "detailed_report",
                "required_inputs": ["document_or_data_source"],
                "confidence": 0.3,
                "error": str(e)
            }
    
    def _generate_extraction_response(self, analysis, query):
        """Generate a response for property extraction requests"""
        system_prompt = """
You are a property extraction specialist for the GasOps Weld Management System. 
You help users understand how to extract properties and what information is available.

Current capabilities:
- Material properties from MTR (Material Test Reports)
- Weld specifications from work orders
- Dimensional data from technical drawings
- Quality inspection results

Note: Currently, this is a demonstration mode. In production, this agent would:
1. Access document repositories
2. Extract structured data using OCR/AI
3. Process technical drawings and specifications
4. Return formatted property data
"""

        user_prompt = f"""
User wants to extract properties. Here's their request: "{query}"

Analysis shows they want: {analysis.get('property_type', 'unknown')} properties
Expected format: {analysis.get('expected_format', 'detailed_report')}

Provide a helpful response explaining:
1. What property extraction capabilities are available
2. What information they would need to provide
3. What format the results would be in
4. Next steps they should take
"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.azure_client.invoke(messages)
            return response.content.strip()
            
        except Exception as e:
            # Fallback response
            property_type = analysis.get('property_type', 'properties')
            return f"""I can help you extract {property_type} from the GasOps system. 

Available extraction capabilities:
• Material Properties - From MTR reports (heat numbers, chemical composition, mechanical properties)
• Weld Specifications - From work orders (weld procedures, materials, dimensions)
• Quality Data - From inspection reports (test results, certifications)
• Technical Specifications - From engineering documents

To extract properties, I would typically need:
- Document ID or reference number
- Specific property names you're looking for
- Preferred output format (table, report, etc.)

This is currently in demonstration mode. In production, I would access your document repository and extract the requested data automatically."""