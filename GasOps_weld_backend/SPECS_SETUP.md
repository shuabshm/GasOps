# Specifications Feature Setup Guide

## Overview

The Specifications (Specs) feature adds RAG (Retrieval Augmented Generation) capabilities to answer questions about gas operations specifications, compliance requirements, and regulatory standards.

## Architecture

The feature uses:
- **Azure Document Intelligence**: Extract text from PDF spec documents
- **Azure AI Search**: Vector database with HNSW algorithm for semantic search
- **Azure OpenAI**: Generate embeddings (text-embedding-ada-002) and answers (GPT-4)
- **SpecsAgent**: Dedicated agent that routes spec-related queries to RAG pipeline

## File Structure

```
GasOps_weld_backend/
├── specs/                          # PDF specification documents (to be added)
├── specs_extracted_texts/          # Extracted text from PDFs
├── tools/
│   ├── specs_extraction.py         # PDF text extraction
│   ├── index_vectorize_specs.py    # Vectorization and indexing
│   └── specs_llm.py                # Semantic search and answer generation
├── agents/
│   └── specs_agent.py              # SpecsAgent handler
├── supervisor/
│   └── supervisor.py               # Updated with SpecsAgent routing
├── main.py                         # Updated to include sources in response
├── test_specs_integration.py       # Integration tests
└── SPECS_SETUP.md                  # This file
```

## Setup Instructions

### Step 1: Verify Environment Variables

Ensure these variables are set in `.env`:

```bash
# Azure OpenAI (for embeddings and chat)
AZURE_OPENAI_ENDPOINT=https://gasops-weld-apiai.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT=gpt-5-chat
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Azure AI Search (for vector storage)
AZURE_SEARCH_ENDPOINT=https://gasops-prod-aisearch-usecase2.search.windows.net
AZURE_SEARCH_KEY=<your-key>
AZURE_SEARCH_DEPLOYMENT=text-embedding-ada-002

# Azure Document Intelligence (for PDF extraction)
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=<your-endpoint>
AZURE_DOCUMENT_INTELLIGENCE_KEY=<your-key>
```

### Step 2: Add Specification PDFs

Two options:

**Option A: Local PDFs**
1. Place PDF files in `specs/` folder
2. Update `tools/specs_extraction.py` to read from local folder (commented code available)

**Option B: Azure Blob Storage** (current default)
1. Upload PDFs to Azure Blob Storage
2. Generate SAS URLs for each PDF
3. Update `pdf_blobs` list in `tools/specs_extraction.py`:

```python
pdf_blobs = [
    {
        "name": "your-spec.pdf",
        "url": "https://your-storage.blob.core.windows.net/container/your-spec.pdf?<SAS-token>"
    }
]
```

### Step 3: Extract Text from PDFs

Run the extraction script to download PDFs and extract text:

```bash
python tools/specs_extraction.py
```

This will:
- Download PDFs from blob storage (or read from local `specs/` folder)
- Use Azure Document Intelligence to extract text
- Save extracted text to `specs_extracted_texts/` folder

**Expected Output:**
```
specs_extracted_texts/
├── G-1065_extracted.txt
└── G-8107StlPipeSpec_extracted.txt
```

### Step 4: Create Vector Index

Run the indexing script to vectorize and upload to Azure AI Search:

```bash
python tools/index_vectorize_specs.py
```

This will:
1. Delete existing `specs-vectorized-index` (if it exists)
2. Create new index with HNSW vector search configuration
3. Read all `*_extracted.txt` files from `specs_extracted_texts/`
4. Chunk text (1000 chars, 100 overlap)
5. Generate embeddings using Azure OpenAI
6. Upload chunks to Azure AI Search

**Expected Output:**
```
Creating index 'specs-vectorized-index'...
Processing G-1065.pdf...
  Split into 15 chunks
  Generating embedding for chunk 1/15...
  ...
Uploading 27 documents to index...
Successfully indexed 27 document chunks!
```

### Step 5: Test the Integration

Run the test script to verify everything works:

```bash
python test_specs_integration.py
```

This will test:
- Supervisor routing to SpecsAgent
- SpecsAgent functionality
- Specs LLM search and answer generation
- End-to-end integration

## Usage

### Via API

Send a POST request to `/ask` endpoint:

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -H "encoded_string: <your-auth-token>" \
  -d '{
    "query": "What welding requirements apply to gas pipelines?",
    "session_id": "test-session"
  }'
```

**Response:**
```json
{
  "answer": "According to G-1065, welders must complete qualification testing...",
  "timestamp": "2025-10-08T12:00:00",
  "context": [...],
  "user_details": {...},
  "decrypted_fields": {...},
  "sources": [
    {
      "document": "G-1065.pdf",
      "chunk": "3/15",
      "page": 12,
      "score": 0.89
    }
  ]
}
```

### Example Questions

The SpecsAgent handles questions about:
- Specifications: "What are the welding specifications for gas pipelines?"
- Requirements: "What's required before a welder can weld?"
- Standards: "What inspection procedures apply?"
- Compliance: "What are the compliance requirements?"
- Procedures: "What are the testing procedures?"

### Non-Spec Questions

Other questions are routed to appropriate agents:
- Work order queries → WeldInsightsAgent
- MTR data queries → MTRAgent
- General questions → Direct answer (no agent)

## How It Works

### Request Flow

```
User Question: "What welding requirements apply to gas pipelines?"
       ↓
1. main.py (/ask endpoint)
       ↓
2. supervisor.py (classify intent with LLM)
   → Intent: SpecsAgent
       ↓
3. agents/specs_agent.py (handle_specs_agent)
       ↓
4. tools/specs_llm.py (ask_question)
   ├─ search_specs()
   │    ├─ Generate question embedding
   │    ├─ Hybrid search (text + vector)
   │    └─ Retrieve top-5 relevant chunks
   │
   └─ generate_answer()
        ├─ Build context from chunks
        ├─ Call GPT with compliance prompt
        └─ Return answer with citations
       ↓
5. Response with answer + sources
```

### Key Features

✅ **Hybrid Search**: Combines keyword + semantic search for better accuracy
✅ **Source Citations**: Always includes document references for traceability
✅ **Compliance Focus**: Low temperature (0.1) for factual, accurate answers
✅ **Chunking Strategy**: Overlap prevents context loss at chunk boundaries
✅ **Semantic Ranking**: Azure AI Search re-ranks results for relevance

## Troubleshooting

### Issue: "Failed to generate embedding"
**Solution:** Check `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` in `.env`

### Issue: "Error searching specs"
**Solution:**
- Verify Azure AI Search credentials in `.env`
- Ensure index `specs-vectorized-index` exists (run `index_vectorize_specs.py`)

### Issue: "No relevant information found"
**Solution:**
- Check if PDFs were extracted (look in `specs_extracted_texts/`)
- Verify index was populated (check Azure AI Search portal)
- Ensure question matches content in spec documents

### Issue: "Index not found"
**Solution:** Run `python tools/index_vectorize_specs.py` to create the index

## Maintenance

### Adding New Specification Documents

1. Add new PDF to blob storage or `specs/` folder
2. Update `pdf_blobs` list in `tools/specs_extraction.py`
3. Run extraction: `python tools/specs_extraction.py`
4. Re-index: `python tools/index_vectorize_specs.py`

### Updating Existing Documents

1. Replace PDF in blob storage or `specs/` folder
2. Run extraction: `python tools/specs_extraction.py`
3. Re-index: `python tools/index_vectorize_specs.py`

### Monitoring

Check Azure AI Search portal to:
- View index statistics
- Monitor query performance
- Analyze search relevance

## Configuration

### Chunking Parameters

In `tools/index_vectorize_specs.py`:
```python
chunk_size = 1000  # Max chunk size in characters
overlap = 100      # Overlap between chunks
```

### Retrieval Parameters

In `tools/specs_llm.py`:
```python
top_k = 5  # Number of chunks to retrieve
temperature = 0.1  # Low for factual accuracy
```

### Search Algorithm

HNSW configuration in `tools/index_vectorize_specs.py`:
```python
"m": 4,
"efConstruction": 400,
"efSearch": 500,
"metric": "cosine"
```

## Security Notes

- PDF SAS URLs should be rotated regularly
- Use Azure Key Vault for production credentials
- Implement rate limiting on `/ask` endpoint
- Monitor Azure OpenAI usage for cost control

## Support

For issues or questions:
1. Check logs: `gasops_weld.log`
2. Run test script: `python test_specs_integration.py`
3. Verify Azure resources in Azure Portal

---

**Status**: Production-ready ✓
**Last Updated**: October 2025
**Version**: 1.0.0
