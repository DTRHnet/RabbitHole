# File: storage/storage.py

"""
RabbitHole/storage/storage.py

Provides high-level functions for managing API keys within the encrypted database.
"""

from storage.database import addApiKey, getAllApiKeys, getApiKeyByLabel
from encryption.encrypt import encryptApiKey
from encryption.decrypt import decryptApiKey
import binascii
import logging

# Spacer for readability
# ------------------------------------------------------------------------------

def loadApiKeys(conn):
    """
    Loads all API key labels from the database.

    Args:
        conn (sqlite.Connection): The SQLite connection object.

    Returns:
        list: A list of dictionaries containing API key labels.
    """
    labels = getAllApiKeys(conn)
    return [{"label": label} for label in labels]

# Spacer for readability
# ------------------------------------------------------------------------------

def retrieveApiKey(conn, label, encryptionKey):
    """
    Retrieves and decrypts the API key corresponding to the given label.

    Args:
        conn (sqlite.Connection): The SQLite connection object.
        label (str): The label of the API key to retrieve.
        encryptionKey (bytes): The encryption key used for decryption.

    Returns:
        str: The decrypted API key, or None if retrieval fails.
    """
    record = getApiKeyByLabel(conn, label)
    if record:
        iv, ciphertext = record
        apiKey = decryptApiKey(iv, ciphertext, encryptionKey)
        if apiKey:
            logging.info(f"API key '{label}' decrypted successfully.")
            return apiKey
        else:
            logging.error(f"Failed to decrypt API key '{label}'.")
            return None
    else:
        logging.warning(f"API key '{label}' does not exist.")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------

def addApiKeySecurely(conn, encryptionKey):
    """
    Securely adds a new API key to the database by encrypting it first.

    Args:
        conn (sqlite.Connection): The SQLite connection object.
        encryptionKey (bytes): The encryption key used for encryption.

    Returns:
        bool: True if the API key was added successfully, False otherwise.
    """
    try:
        import getpass
        label = input("🐰 Enter a label for the API key: ").strip()
        if not label:
            print("🚫 Label cannot be empty.")
            logging.warning("Attempted to add an API key with an empty label.")
            return False

        apiKey = getpass.getpass("🔑 Enter the API key: ").strip()
        if not apiKey:
            print("🚫 API key cannot be empty.")
            logging.warning(f"Attempted to add an API key with an empty value for label '{label}'.")
            return False

        iv, ciphertext = encryptApiKey(apiKey, encryptionKey)
        if iv and ciphertext:
            success = addApiKey(conn, label, iv, ciphertext)
            if success:
                print(f"✅ API key '{label}' stored in your RabbitHole successfully.")
                logging.info(f"API key '{label}' stored in the database.")
                return True
            else:
                print(f"🚫 Failed to store API key '{label}'. It may already exist.")
                return False
        else:
            print("🚫 Encryption failed. API key not stored.")
            return False
    except Exception as e:
        logging.error(f"Exception occurred while adding API key: {e}")
        return False

# Spacer for readability
# ------------------------------------------------------------------------------
