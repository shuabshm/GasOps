"""
MTR Document Processor
Azure Document Intelligence processing for MTR documents
"""
import os
import base64
import tempfile
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

load_dotenv()
logger = logging.getLogger(__name__)

# Azure Document Intelligence configuration
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

class MTRDocumentProcessor:
    def __init__(self):
        """Initialize MTR Document Processor with Azure Document Intelligence credentials"""
        self.endpoint = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
        self.key = AZURE_DOCUMENT_INTELLIGENCE_KEY
        
        if not all([self.endpoint, self.key]):
            raise ValueError("Azure Document Intelligence credentials not found in .env file")
    
    def convert_binary_to_pdf(self, binary_string: str, heat_number: str) -> str:
        """
        Convert binary string to PDF file
        
        Args:
            binary_string (str): Binary string from API response
            heat_number (str): Heat number for file naming
            
        Returns:
            str: Path to the created PDF file
        """
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
            pdf_path = os.path.join(temp_dir, f"{heat_number}.pdf")
            
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_data)
            
            logger.info(f"PDF file created successfully: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Failed to convert binary to PDF for heat number {heat_number}: {str(e)}")
            raise Exception(f"PDF conversion failed: {str(e)}")
    
    def extract_data_with_document_intelligence(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract structured data from PDF using Azure Document Intelligence
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict[str, Any]: Extracted structured data
        """
        try:
            logger.info(f"Processing PDF with Document Intelligence: {pdf_path}")
            
            # Initialize Document Intelligence client
            client = DocumentIntelligenceClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.key)
            )
            
            # Process the document
            with open(pdf_path, 'rb') as f:
                poller = client.begin_analyze_document("prebuilt-document", f)
                result = poller.result()
            
            # Extract key information
            extracted_data = {
                "document_type": "MTR",
                "extraction_method": "Azure Document Intelligence",
                "pdf_source": pdf_path,
                "extracted_fields": self._parse_document_fields(result),
                "extraction_confidence": self._calculate_confidence(result),
                "processing_timestamp": result.created_date_time.isoformat() if result.created_date_time else None,
                "status": "success"
            }
            
            logger.info(f"Document Intelligence extraction completed for {pdf_path}")
            return extracted_data
            
        except Exception as e:
            logger.error(f"Document Intelligence extraction failed for {pdf_path}: {str(e)}")
            raise Exception(f"OCR extraction failed: {str(e)}")
    
    def _parse_document_fields(self, result: AnalyzeResult) -> Dict[str, Any]:
        """Parse document fields from OCR result"""
        fields = {
            "heat_number": None,
            "material_type": None,
            "chemical_composition": {},
            "mechanical_properties": {},
            "test_results": {},
            "manufacturer": None,
            "certification": None,
            "raw_text": ""
        }
        
        # Extract content from pages
        if result.content:
            fields["raw_text"] = result.content
            
            # Look for common MTR fields in the text
            content_lower = result.content.lower()
            
            # Extract heat number
            import re
            heat_patterns = [
                r'heat\s*(?:no|number|#)?\s*:?\s*([A-Z0-9]+)',
                r'heat\s*([A-Z0-9]+)',
                r'lot\s*(?:no|number|#)?\s*:?\s*([A-Z0-9]+)'
            ]
            
            for pattern in heat_patterns:
                match = re.search(pattern, content_lower)
                if match:
                    fields["heat_number"] = match.group(1).upper()
                    break
            
            # Extract chemical composition (look for common elements)
            chemical_patterns = {
                'carbon': r'c\s*:?\s*([\d.]+)',
                'manganese': r'mn\s*:?\s*([\d.]+)',
                'silicon': r'si\s*:?\s*([\d.]+)',
                'phosphorus': r'p\s*:?\s*([\d.]+)',
                'sulfur': r's\s*:?\s*([\d.]+)',
                'chromium': r'cr\s*:?\s*([\d.]+)',
                'nickel': r'ni\s*:?\s*([\d.]+)',
                'molybdenum': r'mo\s*:?\s*([\d.]+)'
            }
            
            for element, pattern in chemical_patterns.items():
                match = re.search(pattern, content_lower)
                if match:
                    fields["chemical_composition"][element] = float(match.group(1))
            
            # Extract mechanical properties
            mechanical_patterns = {
                'tensile_strength': r'tensile.*?(\d+)\s*mpa',
                'yield_strength': r'yield.*?(\d+)\s*mpa',
                'elongation': r'elongation.*?(\d+)\s*%',
                'hardness': r'hardness.*?(\d+)'
            }
            
            for prop, pattern in mechanical_patterns.items():
                match = re.search(pattern, content_lower)
                if match:
                    fields["mechanical_properties"][prop] = int(match.group(1))
        
        return fields
    
    def _calculate_confidence(self, result: AnalyzeResult) -> float:
        """Calculate overall confidence score from OCR result"""
        if not result.pages:
            return 0.0
        
        total_confidence = 0.0
        confidence_count = 0
        
        for page in result.pages:
            if page.words:
                for word in page.words:
                    if hasattr(word, 'confidence') and word.confidence is not None:
                        total_confidence += word.confidence
                        confidence_count += 1
        
        return total_confidence / confidence_count if confidence_count > 0 else 0.0
    
    def cleanup_temp_file(self, file_path: str):
        """
        Clean up temporary PDF file
        
        Args:
            file_path (str): Path to the file to be deleted
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary file {file_path}: {str(e)}")
    
    def process_mtr_document(self, binary_string: str, heat_number: str, company_mtr_file_id: str) -> Dict[str, Any]:
        """
        Complete MTR document processing pipeline
        
        Args:
            binary_string (str): Binary string from API
            heat_number (str): Heat number
            company_mtr_file_id (str): Company MTR File ID
            
        Returns:
            Dict[str, Any]: Processed MTR data ready for database storage
        """
        pdf_path = None
        try:
            # Step 1: Convert binary to PDF
            pdf_path = self.convert_binary_to_pdf(binary_string, heat_number)
            
            # Step 2: Extract data using Document Intelligence
            extracted_data = self.extract_data_with_document_intelligence(pdf_path)
            
            # Step 3: Prepare data for response
            processed_data = {
                "heatNumber": heat_number,
                "companyMTRFileID": company_mtr_file_id,
                "extractedData": extracted_data,
                "processingStatus": "success",
                "extractionTimestamp": extracted_data.get("processing_timestamp"),
                "extractionConfidence": extracted_data.get("extraction_confidence", 0.0)
            }
            
            logger.info(f"MTR document processing completed successfully for heat number {heat_number}")
            return processed_data
            
        except Exception as e:
            logger.error(f"MTR document processing failed: {str(e)}")
            raise e
        finally:
            # Always clean up temporary files
            if pdf_path:
                self.cleanup_temp_file(pdf_path)

# Convenience functions for tool use
def process_mtr_document(binary_string: str, heat_number: str, company_mtr_file_id: str) -> Dict[str, Any]:
    """
    Convenience function to process MTR document
    
    Args:
        binary_string (str): Binary string from API
        heat_number (str): Heat number
        company_mtr_file_id (str): Company MTR File ID
        
    Returns:
        Dict[str, Any]: Processed MTR data
    """
    processor = MTRDocumentProcessor()
    return processor.process_mtr_document(binary_string, heat_number, company_mtr_file_id)