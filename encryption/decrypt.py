# File: encryption/decrypt.py

"""
RabbitHole/encryption/decrypt.py

Handles decryption of API keys using AES-GCM.
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import logging

# Spacer for readability
# ------------------------------------------------------------------------------

def decryptApiKey(iv, ciphertext, key):
    """
    Decrypts the given ciphertext using AES-GCM with the provided key and IV.

    Args:
        iv (str): The base64-encoded initialization vector.
        ciphertext (str): The base64-encoded ciphertext to decrypt.
        key (bytes): The decryption key.

    Returns:
        str: The decrypted API key as a string, or None if decryption fails.
    """
    try:
        aesgcm = AESGCM(key)
        ivBytes = base64.b64decode(iv)
        ciphertextBytes = base64.b64decode(ciphertext)
        decrypted = aesgcm.decrypt(ivBytes, ciphertextBytes, None)
        apiKey = decrypted.decode()
        logging.info("API key decrypted successfully.")
        return apiKey
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------
