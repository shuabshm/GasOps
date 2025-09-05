import os
from typing import List, Dict, Optional
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class AISearchClient:
    def __init__(self):
        """Initialize AI Search client for specs/MTR document search"""
        try:
            # Azure AI Search configuration
            self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
            self.search_key = os.getenv("AZURE_SEARCH_KEY")
            self.index_name = "specs-vectorized-index"  # Same as gasops_secondusecase
            
            # Azure OpenAI configuration
            azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
            azure_openai_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
            self.embedding_deployment = os.getenv("AZURE_SEARCH_DEPLOYMENT")  # embedding model
            self.chat_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # GPT model
            
            if not all([self.search_endpoint, self.search_key, azure_openai_key, self.embedding_deployment]):
                raise ValueError("Missing required environment variables for AI Search")
            
            # Initialize clients
            self.openai_client = AzureOpenAI(
                azure_endpoint=azure_openai_endpoint,
                api_key=azure_openai_key,
                api_version=azure_openai_version
            )
            
            self.search_client = SearchClient(
                endpoint=self.search_endpoint,
                index_name=self.index_name,
                credential=AzureKeyCredential(self.search_key)
            )
            
            logger.info("AI Search client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Search client: {str(e)}")
            raise e
    
    def get_question_embedding(self, question: str) -> List[float]:
        """Generate embedding for the user question"""
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_deployment,
                input=question
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding for question: {e}")
            return []
    
    def search_specs(self, question: str, top_k: int = 5) -> List[Dict]:
        """Search the specs index for relevant chunks"""
        
        # Get embedding for the question
        question_vector = self.get_question_embedding(question)
        
        if not question_vector:
            logger.error("Failed to generate embedding for question")
            return []
        
        try:
            # Perform vector similarity search
            results = self.search_client.search(
                search_text=question,  # Also include text search
                vector_queries=[{
                    "kind": "vector",
                    "vector": question_vector,
                    "k_nearest_neighbors": top_k,
                    "fields": "embeddingVector"
                }],
                select=["id", "content", "documentName", "chunkNumber", "totalChunks", "pageNumber"],
                top=top_k,
                query_type="semantic",
                semantic_configuration_name="my-semantic-config"
            )
            
            # Extract results
            search_results = []
            for result in results:
                search_results.append({
                    "content": result["content"],
                    "document_name": result["documentName"],
                    "chunk_number": result["chunkNumber"],
                    "total_chunks": result["totalChunks"],
                    "page_number": result["pageNumber"],
                    "score": result.get("@search.score", 0)
                })
            
            logger.info(f"Found {len(search_results)} relevant chunks for question")
            return search_results
        
        except Exception as e:
            logger.error(f"Error searching specs: {e}")
            return []
    
    def generate_answer(self, question: str, search_results: List[Dict]) -> str:
        """Generate answer using GPT with the retrieved context"""
        
        if not search_results:
            return "I couldn't find any relevant information in the specifications to answer your question."
        
        # Prepare context from search results
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(
                f"Context {i} (from {result['document_name']}, chunk {result['chunk_number']}/{result['total_chunks']}, page {result['page_number']}):\n"
                f"{result['content']}\n"
            )
        
        context = "\n".join(context_parts)
        
        # System prompt for MTR/material property analysis
        system_prompt = """You are an expert assistant for MTR (Material Test Report) and material property analysis. Use only the provided specification excerpts to answer questions about material properties, chemical composition, mechanical properties, and technical specifications.

IMPORTANT INSTRUCTIONS:
1. Answer ONLY based on the provided context from specifications
2. Always include specific section references and page citations when available
3. If the information is not in the provided specifications, say "Not specified in the provided specifications"
4. Be precise and cite the exact document name and section when possible
5. For property questions, provide exact values when found (e.g., "Carbon (C): 0.18%")
6. If you're unsure or the context is ambiguous, clearly state your uncertainty
7. Format citations as: (Page X, [Document Name], Section Y.Z if available)

Focus on material properties, welding requirements, chemical composition, mechanical properties, and technical specifications."""

        # User prompt with question and context
        user_prompt = f"""Question: {question}

Context from specifications:
{context}

Please provide a detailed answer about the material properties or technical specifications based only on the above context, including proper citations."""

        try:
            # Generate response using GPT
            response = self.openai_client.chat.completions.create(
                model=self.chat_deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for factual accuracy
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "I encountered an error while generating the answer. Please try again."
    
    def search_and_answer(self, question: str, top_k: int = 5) -> Dict:
        """Main function to search specs and answer questions about material properties"""
        
        logger.info(f"Processing question: {question}")
        
        # Step 1: Search for relevant chunks
        search_results = self.search_specs(question, top_k)
        
        if not search_results:
            return {
                "success": False,
                "question": question,
                "answer": "I couldn't find any relevant information in the specifications to answer your question.",
                "sources": [],
                "method": "ai_search"
            }
        
        logger.info(f"Found {len(search_results)} relevant chunks")
        
        # Step 2: Generate answer using GPT
        logger.info("Generating answer from specifications...")
        answer = self.generate_answer(question, search_results)
        
        # Prepare sources for citation
        sources = []
        for result in search_results:
            sources.append({
                "document": result['document_name'],
                "chunk": f"{result['chunk_number']}/{result['total_chunks']}",
                "page": result['page_number'],
                "score": result['score']
            })
        
        return {
            "success": True,
            "question": question,
            "answer": answer,
            "sources": sources,
            "method": "ai_search"
        }