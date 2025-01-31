# File: encryption/encrypt.py

"""
RabbitHole/encryption/encrypt.py

Handles encryption of API keys using AES-GCM.
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import logging

# Spacer for readability
# ------------------------------------------------------------------------------

def deriveKey(password, salt):
    """
    Derives a cryptographic key from the given password and salt using PBKDF2.

    Args:
        password (str): The user's password.
        salt (bytes): A unique salt.

    Returns:
        bytes: The derived cryptographic key.
    """
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend

    try:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 key size
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        logging.info("Encryption key derived successfully.")
        return key
    except Exception as e:
        logging.error(f"Key derivation failed: {e}")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------

def getEncryptionKey(password):
    """
    Retrieves or generates the encryption key based on the user's password.

    Args:
        password (str): The user's password.

    Returns:
        bytes: The derived encryption key, or None if derivation fails.
    """
    saltFile = 'config/salt.bin'
    if not os.path.exists(saltFile):
        salt = os.urandom(16)
        try:
            with open(saltFile, 'wb') as f:
                f.write(salt)
            logging.info("Generated new salt for key derivation.")
        except Exception as e:
            logging.error(f"Failed to write salt file: {e}")
            return None
    else:
        try:
            with open(saltFile, 'rb') as f:
                salt = f.read()
            logging.info("Loaded existing salt for key derivation.")
        except Exception as e:
            logging.error(f"Failed to read salt file: {e}")
            return None

    # Derive the key using the password and salt
    key = deriveKey(password, salt)
    return key

# Spacer for readability
# ------------------------------------------------------------------------------

def encryptApiKey(apiKey, key):
    """
    Encrypts the given API key using AES-GCM with the provided key.

    Args:
        apiKey (str): The plaintext API key to encrypt.
        key (bytes): The encryption key.

    Returns:
        tuple: A tuple containing the base64-encoded IV and ciphertext.
    """
    try:
        aesgcm = AESGCM(key)
        iv = os.urandom(12)  # 96-bit nonce for GCM
        ciphertext = aesgcm.encrypt(iv, apiKey.encode(), None)
        ivB64 = base64.b64encode(iv).decode()
        ciphertextB64 = base64.b64encode(ciphertext).decode()
        logging.info("API key encrypted successfully.")
        return ivB64, ciphertextB64
    except Exception as e:
        logging.error(f"Encryption failed: {e}")
        return None, None

# Spacer for readability
# ------------------------------------------------------------------------------
