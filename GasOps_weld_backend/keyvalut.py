from azure.identity import DefaultAzureCredential, ClientSecretCredential, InteractiveBrowserCredential
from azure.keyvault.secrets import SecretClient
import os

# Define your Key Vault URL
key_vault_url = "https://gasops-prod-ai-keyvault.vault.azure.net"

# Try multiple authentication methods
def get_credential():
    # Tenant ID from the error message
    tenant_id = "738de1b6-4c08-4620-88ba-3bf05dbef12f"
    
    try:
        # Try DefaultAzureCredential first with tenant configured
        credential = DefaultAzureCredential(additionally_allowed_tenants=[tenant_id])
        # Test the credential by trying to get a token
        credential.get_token("https://vault.azure.net/.default")
        print("Successfully authenticated using DefaultAzureCredential")
        return credential
    except Exception as e:
        print(f"DefaultAzureCredential failed: {e}")
        
        # Try InteractiveBrowserCredential as fallback
        try:
            print("Trying InteractiveBrowserCredential...")
            credential = InteractiveBrowserCredential(additionally_allowed_tenants=[tenant_id])
            credential.get_token("https://vault.azure.net/.default")
            print("Successfully authenticated using InteractiveBrowserCredential")
            return credential
        except Exception as e2:
            print(f"InteractiveBrowserCredential failed: {e2}")
            
            # Try with wildcard tenant access
            try:
                print("Trying InteractiveBrowserCredential with wildcard tenants...")
                credential = InteractiveBrowserCredential(additionally_allowed_tenants=["*"])
                credential.get_token("https://vault.azure.net/.default")
                print("Successfully authenticated using InteractiveBrowserCredential with wildcard")
                return credential
            except Exception as e3:
                print(f"InteractiveBrowserCredential with wildcard failed: {e3}")
                raise Exception("All authentication methods failed")

try:
    # Get authenticated credential
    credential = get_credential()
    
    # Create a SecretClient
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
    
    # Retrieve secrets (match names from your Key Vault configuration)
    print("Retrieving secrets from Key Vault...")
    
    # Azure OpenAI 1
    AZURE_OPENAI_ENDPOINT = secret_client.get_secret("AZUREOPENAIENDPOINT11").value
    AZURE_OPENAI_API_KEY = secret_client.get_secret("AZUREOPENAIAPIKEY1").value
    AZURE_OPENAI_DEPLOYMENT = secret_client.get_secret("AZUREOPENAIDEPLOYMENT1").value
    AZURE_OPENAI_MODEL_NAME = secret_client.get_secret("AZUREOPENAIMODELNAME1").value
    AZURE_OPENAI_API_VERSION = secret_client.get_secret("AZUREOPENAIAPIVERSION1").value

    # Azure AI Search (commented out)
    # AZURE_SEARCH_API_VERSION = secret_client.get_secret("AZURESEARCHAPIVERSION").value
    # AZURE_SEARCH_DEPLOYMENT = secret_client.get_secret("AZURESEARCHDEPLOYMENT2").value
    # AZURE_SEARCH_ENDPOINT = secret_client.get_secret("AZURESEARCHENDPOINT2").value
    # AZURE_SEARCH_KEY = secret_client.get_secret("AZURESEARCHKEY2").value

    # Azure Document Intelligence
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = secret_client.get_secret("AZUREDOCUMENTINTELLIGENCEENDPOINT").value
    AZURE_DOCUMENT_INTELLIGENCE_KEY = secret_client.get_secret("AZUREDOCUMENTINTELLIGENCEKEY").value

    # Database credentials
    SERVER = secret_client.get_secret("SERVER").value
    DATABASE_OAMSCM = secret_client.get_secret("DATABASEOAMSCM").value
    USERNAME = secret_client.get_secret("USERNAME").value
    PASSWORD = secret_client.get_secret("PASSWORD").value

    # Example usage
    print("\n=== Retrieved Secrets ===")
    print(f"OpenAI Endpoint : {AZURE_OPENAI_ENDPOINT}")
    print(f"OpenAI Key : {AZURE_OPENAI_API_KEY}")
    print(f"OpenAI Deployment : {AZURE_OPENAI_DEPLOYMENT}")
    print(f"OpenAI Model Name : {AZURE_OPENAI_MODEL_NAME}")
    print(f"OpenAI API Version : {AZURE_OPENAI_API_VERSION}")
    print(f"Database Connection: Server={SERVER}, DB={DATABASE_OAMSCM}, User={USERNAME}")
    # print(f"Search Endpoint: {AZURE_SEARCH_ENDPOINT}, Deployment: {AZURE_SEARCH_DEPLOYMENT}")
    print(f"Document Intelligence Endpoint: {AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT}")
    print(f"Document Intelligence Key: {AZURE_DOCUMENT_INTELLIGENCE_KEY}")

except Exception as e:
    print(f"Error accessing Key Vault: {e}")
    print("Please ensure you are authenticated to Azure and have access to the Key Vault.")
    print("You can try:")
    print("1. az login (if Azure CLI is installed)")
    print("2. Ensure your account has access to the Key Vault")
    print("3. Check if the Key Vault URL and secret names are correct")