# File: auth/oauth.py

"""
RabbitHole/auth/oauth.py

Handles OAuth 2.0 based authentication.
"""

import logging
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

# Spacer for readability
# ------------------------------------------------------------------------------

def authenticateWithOAuth(clientId, clientSecret, tokenUrl, scope=None):
    """
    Authenticates the user using OAuth 2.0 Client Credentials Grant.

    Args:
        clientId (str): The OAuth client ID.
        clientSecret (str): The OAuth client secret.
        tokenUrl (str): The URL to obtain the OAuth token.
        scope (list, optional): The scope of the OAuth token.

    Returns:
        dict: The OAuth token if authentication is successful, None otherwise.
    """
    try:
        client = BackendApplicationClient(client_id=clientId)
        oauth = OAuth2Session(client=client, scope=scope)
        token = oauth.fetch_token(token_url=tokenUrl, client_id=clientId, client_secret=clientSecret)
        logging.info("OAuth authentication successful.")
        return token
    except Exception as e:
        logging.error(f"OAuth authentication failed: {e}")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------
