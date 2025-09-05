"""
MTR Agent for extracting specific properties, measurements, and technical specifications
Uses OCR extraction from MTR documents and AI knowledge for compliance validation
"""
from langchain.schema import HumanMessage, SystemMessage
import json
import asyncio
import os
import tempfile
import base64
from azure_client import get_azure_chat_openai
from api_client import APIClient
import logging

# Azure Document Intelligence imports
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class MTRAgent:
    def __init__(self):
        try:
            self.azure_client = get_azure_chat_openai()
            logger.info("MTR agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
            raise e
    
    async def process(self, query, auth_token):
        """Process MTR queries using OCR extraction and AI knowledge for compliance"""
        try:
            logger.info(f"Processing MTR query: {query}")
            
            # Step 1: Extract parameters from user query
            parameters = self._extract_query_parameters(query)
            logger.info(f"Extracted parameters: {parameters}")
            
            heat_number = parameters.get("heat_number")
            company_mtr_file_id = parameters.get("company_mtr_file_id")
            
            # Step 2: Heat number is required for MTR agent
            if not heat_number:
                return {
                    "success": False,
                    "error": "Heat number is required for MTR document queries.",
                    "agent": "MTR agent",
                    "apis_called": []
                }
            
            logger.info("Processing heat-number specific query with OCR extraction")
            return await self._process_with_ocr(query, heat_number, company_mtr_file_id, auth_token)
            
        except Exception as e:
            logger.error(f"MTR Agent processing failed: {str(e)}")
            return {
                "success": False, 
                "error": str(e), 
                "agent": "MTR agent",
                "apis_called": []
            }
    
    async def _process_with_ocr(self, query, heat_number, company_mtr_file_id, auth_token):
        """Process query using OCR extraction from specific MTR document"""
        try:
            # Create API client with auth token
            api_client = APIClient()
            api_client.auth_token = auth_token
            
            logger.info(f"Getting MTR file data for heat number: {heat_number}")
            result = await self._get_mtr_file_and_extract_properties(api_client, heat_number, company_mtr_file_id, query)
            
            return result
            
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            return {
                "success": False,
                "error": f"MTR document processing failed: {str(e)}",
                "agent": "MTR agent",
                "apis_called": []
            }
    
    def _extract_query_parameters(self, query):
        """Extract heat number and company MTR file ID from user query using AI"""
        extraction_prompt = f"""
You are analyzing a conversational MTR (Material Test Report) query that may include previous conversation context. Your task is to extract material identifiers from the ENTIRE query text, including previous messages.

FULL QUERY TEXT (including previous conversation context):
"{query}"

EXTRACTION TASK:
1. **Heat Number (required)**: Look throughout the entire query text for ANY material identifiers, including:
   - Explicit heat numbers (e.g., "heat number 18704220")
   - Material codes/IDs (e.g., "W4A789", "12345ABC")  
   - Alphanumeric identifiers mentioned in previous messages
   - Material references from earlier conversation context

2. **Company MTR File ID (optional)**: Look for file IDs, document IDs, or reference numbers

CONTEXT UNDERSTANDING:
- If current question is about "compliance", "requirements", "API 5L", "standards" etc., look for material identifiers mentioned EARLIER in the conversation
- Previous messages may contain the material identifier that the current question refers to
- Example: Previous message mentions "W4A789 properties", current question "does it satisfy API 5L requirement?" → Heat number is "W4A789"

IMPORTANT: 
- Analyze the FULL query text including all previous messages
- Current question may refer to materials discussed earlier
- Look for ANY alphanumeric codes that could be material identifiers
- If you find a material identifier ANYWHERE in the query text, extract it

Respond with JSON only:
{{
    "heat_number": "extracted_heat_number_or_null",
    "company_mtr_file_id": "extracted_company_id_or_null",
    "confidence": 0.95
}}
"""
        
        try:
            messages = [
                SystemMessage(content="You are a parameter extraction specialist. Respond only with valid JSON."),
                HumanMessage(content=extraction_prompt)
            ]
            
            response = self.azure_client.invoke(messages)
            parameters_text = response.content.strip()
            parameters = json.loads(parameters_text)
            
            # Clean up null values
            if parameters.get("heat_number") in ["null", None, ""]:
                parameters["heat_number"] = None
            if parameters.get("company_mtr_file_id") in ["null", None, ""]:
                parameters["company_mtr_file_id"] = None
                
            return parameters
            
        except Exception as e:
            logger.warning(f"Parameter extraction failed: {str(e)}")
            # Simple fallback
            return {
                "heat_number": None,
                "company_mtr_file_id": None,
                "confidence": 0.1,
                "extraction_method": "fallback",
                "error": str(e)
            }
    
    def _convert_binary_to_pdf(self, binary_string: str, heat_number: str) -> str:
        """Convert binary string to PDF file"""
        try:
            # Try to decode as base64 first
            try:
                pdf_data = base64.b64decode(binary_string)
                logger.info(f"Successfully decoded binary string as base64 for heat number {heat_number}")
            except Exception:
                # If base64 decoding fails, assume it's raw binary
                pdf_data = binary_string.encode('latin-1') if isinstance(binary_string, str) else binary_string
                logger.info(f"Using binary string as raw data for heat number {heat_number}")
            
            # Create temporary file with heat number as name
            temp_dir = tempfile.gettempdir()
            pdf_path = os.path.join(temp_dir, f"MTR_{heat_number}.pdf")
            
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_data)
            
            logger.info(f"PDF file created successfully: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Failed to convert binary to PDF for heat number {heat_number}: {str(e)}")
            raise Exception(f"PDF conversion failed: {str(e)}")
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using Azure Document Intelligence"""
        try:
            # Get credentials from environment
            endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
            key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
            
            if not endpoint or not key:
                raise ValueError("Azure Document Intelligence credentials not found in .env file")
            
            client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
            
            # Read the PDF file as binary data and pass directly to API
            with open(pdf_path, "rb") as f:
                poller = client.begin_analyze_document(
                    "prebuilt-read",  # Use prebuilt-read for text extraction
                    body=f  # Pass the file object directly as body
                )
            
            result: AnalyzeResult = poller.result()
            
            # Extract text content directly from the result
            text_content = result.content if result.content else ""
            
            # Alternative: If you want to extract text line by line
            if not text_content and result.pages:
                all_text = []
                for page in result.pages:
                    if page.lines:
                        for line in page.lines:
                            all_text.append(line.content)
                text_content = "\n".join(all_text)
            
            logger.info(f"Successfully extracted {len(text_content)} characters of text from PDF")
            return text_content
            
        except Exception as e:
            logger.error(f"Text extraction failed for {pdf_path}: {str(e)}")
            raise Exception(f"OCR extraction failed: {str(e)}")
    
    def _answer_property_question(self, query: str, extracted_text: str, document_info: dict) -> str:
        """Use LLM to answer property questions from extracted text"""
        prompt = f"""
You are an expert assistant for MTR (Material Test Report) analysis. The following is the extracted text from an MTR document:

Document Information:
- File: {document_info.get('FileName', 'Unknown')}
- Material: {document_info.get('Material', 'Unknown')}
- Size: {document_info.get('Size', 'Unknown')}
- Manufacturer: {document_info.get('Manufacturer', 'Unknown')}

---
Extracted Text from MTR Document:
{extracted_text}
---

The user has the following question about this MTR document:
"{query}"

Rules:
1. First understand the user's question about specific properties (chemical composition, mechanical properties, etc.)
2. Search through the extracted text to find the relevant information
3. If the user asks about specific values like carbon content, look for chemical composition tables or sections
4. For property questions, provide exact values when found (e.g., "Carbon (C): 0.18%")
5. If the information is not clearly found in the document, state that clearly
6. If you find the information, explain where it was found (e.g., "From the chemical composition section...")
7. Be precise and technical in your response

Important: Do not include "Source:" information at the end of your response.

Answer:
"""
        
        try:
            messages = [
                SystemMessage(content="You are an expert MTR document analyst. Provide accurate, precise technical information."),
                HumanMessage(content=prompt)
            ]
            
            response = self.azure_client.invoke(messages)
            return response.content.strip()
            
        except Exception as e:
            logger.warning(f"LLM response generation failed: {str(e)}")
            return f"I was able to extract text from the MTR document, but encountered an issue analyzing it. The document contains information about {document_info.get('Material', 'the material')} from {document_info.get('Manufacturer', 'the manufacturer')}."
    
    async def _get_mtr_file_and_extract_properties(self, api_client, heat_number, company_mtr_file_id, query):
        """Get MTR file data and extract properties using OCR"""
        apis_called = []
        
        try:
            # Step 1: Get PDF binary data using GetMTRFileDatabyHeatNumber API
            logger.info(f"Calling GetMTRFileDatabyHeatNumber API for heat number: {heat_number}")
            apis_called.append("/api/AIMTRMetaData/GetMTRFileDatabyHeatNumber")
            pdf_result = api_client.get_mtr_file_data_by_heat_number(heat_number, company_mtr_file_id)
            
            if not pdf_result.get("success"):
                return {
                    "success": False,
                    "error": "Unable to connect to database for MTR file retrieval",
                    "agent": "MTR agent",
                    "apis_called": apis_called
                }
            
            pdf_data = pdf_result.get("data")
            if not pdf_data or not pdf_data.get("Obj"):
                return {
                    "success": False,
                    "error": f"No MTR document found for heat number {heat_number}",
                    "agent": "MTR agent",
                    "apis_called": apis_called
                }
            
            # Process only the first document found
            first_obj = pdf_data.get("Obj", [])[0]
            binary_string = first_obj.get("BinaryString")
            file_company_mtr_id = str(first_obj.get("CompanyMTRFileID", ""))
            file_name = first_obj.get("FileName", "")
            
            if not binary_string:
                return {
                    "success": False,
                    "error": f"No binary data found in MTR document for heat number {heat_number}",
                    "agent": "MTR agent",
                    "apis_called": apis_called
                }
            
            logger.info(f"Processing MTR document: {file_name} (CompanyMTRFileID: {file_company_mtr_id})")
            logger.info(f"Total documents available: {pdf_data.get('Count', 0)}, processing first one only")
            
            # Step 2: Convert binary string to PDF and extract text
            pdf_path = None
            try:
                pdf_path = self._convert_binary_to_pdf(binary_string, heat_number)
                
                # Add Document Intelligence API call
                apis_called.append("/documentintelligence/analyze")
                extracted_text = self._extract_text_from_pdf(pdf_path)
                
                if not extracted_text:
                    return {
                        "success": False,
                        "error": "Unable to extract text from MTR document",
                        "agent": "MTR agent",
                        "apis_called": apis_called
                    }
                
                # Step 3: Use LLM to answer property question from extracted text
                apis_called.append("/openai/chat/completions")
                response = self._answer_property_question(query, extracted_text, first_obj)
                
                return {
                    "success": True,
                    "data": response,
                    "agent": "MTR agent",
                    "apis_called": apis_called
                }
                
            except Exception as e:
                logger.error(f"OCR processing failed: {str(e)}")
                return {
                    "success": False,
                    "error": f"Unable to extract data from document: {str(e)}",
                    "agent": "MTR agent",
                    "apis_called": apis_called
                }
            finally:
                # Clean up temporary PDF file
                if pdf_path and os.path.exists(pdf_path):
                    try:
                        os.remove(pdf_path)
                        logger.info(f"Cleaned up temporary file: {pdf_path}")
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"MTR file processing failed: {str(e)}")
            return {
                "success": False,
                "error": f"MTR document processing failed: {str(e)}",
                "agent": "MTR agent",
                "apis_called": apis_called
            }