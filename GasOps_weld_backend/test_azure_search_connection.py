"""
Test Azure AI Search Connection

This script verifies that your Azure AI Search service is accessible
and ready to use for the specs feature.
"""
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

# Load environment variables
load_dotenv()

# Load credentials
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")

print("\n" + "="*80)
print("AZURE AI SEARCH CONNECTION TEST")
print("="*80)
print(f"\nEndpoint: {search_endpoint}")
print(f"Key: {'*' * 40}{search_key[-4:] if search_key else 'NOT SET'}")
print("\n" + "="*80)

# Check if credentials are set
if not search_endpoint:
    print("\n[ERROR] AZURE_SEARCH_ENDPOINT is not set in .env file")
    exit(1)

if not search_key:
    print("\n[ERROR] AZURE_SEARCH_KEY is not set in .env file")
    exit(1)

# Test connection
print("\nTesting connection...")

try:
    # Create client
    client = SearchIndexClient(
        endpoint=search_endpoint,
        credential=AzureKeyCredential(search_key)
    )

    # List indexes
    print("[SUCCESS] Connection successful!\n")

    print("Fetching existing indexes...")
    indexes = list(client.list_indexes())

    if indexes:
        print(f"\n[SUCCESS] Found {len(indexes)} existing index(es):")
        for idx in indexes:
            print(f"  - {idx.name} ({len(idx.fields)} fields)")
    else:
        print("\n[SUCCESS] No indexes found yet (this is normal for a new search service)")
        print("  The index will be created when you run: python tools/index_vectorize_specs.py")

    print("\n" + "="*80)
    print("[SUCCESS] AZURE AI SEARCH IS READY TO USE!")
    print("="*80)
    print("\nNext steps:")
    print("1. Add PDF files to specs/ folder")
    print("2. Run: python tools/specs_extraction.py (extract text from PDFs)")
    print("3. Run: python tools/index_vectorize_specs.py (create index and upload)")
    print("="*80 + "\n")

except Exception as e:
    print(f"\n[FAILED] CONNECTION FAILED!")
    print(f"\nError: {e}")
    print("\n" + "="*80)
    print("TROUBLESHOOTING:")
    print("="*80)
    print("1. Check AZURE_SEARCH_ENDPOINT in .env file")
    print("   Format: https://your-service-name.search.windows.net")
    print("\n2. Check AZURE_SEARCH_KEY in .env file")
    print("   - Go to Azure Portal > Your Search Service > Keys")
    print("   - Copy the Primary admin key")
    print("\n3. Verify your Azure AI Search service is running")
    print("   - Check Azure Portal > Your Search Service > Overview")
    print("="*80 + "\n")
    exit(1)
