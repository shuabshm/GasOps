# Token Decryption and Authentication Module
# Handles base64 token decoding, credential extraction, and authentication token generation
# Provides secure token management for multi-tenant organization access

import base64
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

def decode(encoded_string):
    """
    Decode a base64 encoded string containing organization credentials.

    Args:
        encoded_string (str): The base64 encoded string to decode

    Returns:
        dict: Decoded credentials with LoginMasterID, Database_Name, and OrgID

    Raises:
        Exception: If decoding fails or string format is invalid
    """
    try:
        # Decode the base64 string
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')

        # Parse the decoded string (format: LoginMasterID&Database_Name&OrgID)
        decoded_items = decoded_string.split('&')

        if len(decoded_items) != 3:
            raise ValueError(f"Invalid token format: expected 3 parts, got {len(decoded_items)}")

        decoded_dict = {
            "LoginMasterID": decoded_items[0],
            "Database_Name": decoded_items[1],
            "OrgID": decoded_items[2]
        }

        logger.info("Successfully decoded organization credentials")
        return decoded_dict

    except Exception as e:
        logger.error(f"Failed to decode credentials: {str(e)}")
        raise

def generate_auth_token(login_master_id, database_name, org_id):
    """
    Generate authentication token for API calls with expiration timestamp.

    Creates a time-bound authentication token containing user credentials
    and expiration information for secure API access.

    Args:
        login_master_id (str): Login Master ID from decoded credentials
        database_name (str): Database name for the organization
        org_id (str): Organization identifier

    Returns:
        str: Base64 encoded authentication token with format:
             {expiry_date}&{login_id}&{db_name}&{creation_date}&{org_id}

    Raises:
        Exception: If token generation fails
    """
    try:
        now_utc = datetime.now(timezone.utc)
        date_plus_one = (now_utc + timedelta(days=1)).isoformat()
        date_now = now_utc.isoformat()

        # Format: expiry&login_id&database&creation&org_id
        token_str = f"{date_plus_one}&{login_master_id}&{database_name}&{date_now}&{org_id}"

        def encode_base64(text: str) -> str:
            """Encode text to base64 string."""
            if text is None:
                return None
            text_bytes = text.encode('utf-8')
            return base64.b64encode(text_bytes).decode('utf-8')

        encoded_token = encode_base64(token_str)
        logger.info("Successfully generated authentication token")
        return encoded_token

    except Exception as e:
        logger.error(f"Failed to generate authentication token: {str(e)}")
        raise

