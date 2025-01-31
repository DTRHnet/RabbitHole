# File: auth/password.py

"""
RabbitHole/auth/password.py

Handles password-based authentication.
"""

import bcrypt
import logging
from storage.database import getStoredPasswordHash

# Spacer for readability
# ------------------------------------------------------------------------------

def verifyPassword(storedHash, password):
    """
    Verifies a plaintext password against the stored bcrypt hash.

    Args:
        storedHash (bytes): The stored bcrypt hashed password.
        password (str): The plaintext password to verify.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Compare the provided password with the stored hash
    return bcrypt.checkpw(password.encode(), storedHash)

# Spacer for readability
# ------------------------------------------------------------------------------

def authenticateUser(conn):
    """
    Authenticates the user by verifying their password.

    Args:
        conn (sqlite.Connection): The SQLite connection object.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    # Prompt the user for their password
    import getpass
    password = getpass.getpass("🔒 Enter your secret password: ")

    # Retrieve the stored password hash from the database
    storedHash = getStoredPasswordHash(conn)
    if storedHash is None:
        logging.error("No stored password hash found.")
        return False

    # Verify the provided password against the stored hash
    if verifyPassword(storedHash, password):
        logging.info("User authenticated successfully.")
        return True
    else:
        logging.warning("User failed to authenticate.")
        return False

# Spacer for readability
# ------------------------------------------------------------------------------
