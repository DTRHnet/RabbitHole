# File: storage/database.py

"""
RabbitHole/storage/database.py

Handles interactions with the encrypted SQLite database.
Manages both API keys and user authentication data.
"""

import sqlcipher3 as sqlite
import logging
import os
import bcrypt
import binascii  # Added import

# Spacer for readability
# ------------------------------------------------------------------------------

def initializeDatabase(dbPath, key):
    """
    Initializes the encrypted SQLite database. Creates the 'api_keys' and 'users' tables if they don't exist.

    Args:
        dbPath (str): The path to the SQLite database file.
        key (bytes): The encryption key for SQLCipher.

    Returns:
        sqlite.Connection: The SQLite connection object, or None if initialization fails.
    """
    dbExists = os.path.exists(dbPath)
    try:
        conn = sqlite.connect(dbPath)
        cursor = conn.cursor()
        
        # Convert the binary key to hexadecimal
        key_hex = binascii.hexlify(key).decode('utf-8')
        
        # Set the PRAGMA key using hexadecimal representation within double quotes
        cursor.execute(f'PRAGMA key = "x\'{key_hex}\'";')  # Modified line
        logging.info(f"Set PRAGMA key for database '{dbPath}'.")  # Modified line
        
        if not dbExists:
            # Create the 'api_keys' table
            cursor.execute("""
                CREATE TABLE api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT UNIQUE NOT NULL,
                    iv TEXT NOT NULL,
                    ciphertext TEXT NOT NULL
                );
            """)
            logging.info("Created 'api_keys' table in the RabbitHole database.")
            
            # Create the 'users' table
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password_hash TEXT NOT NULL
                );
            """)
            logging.info("Created 'users' table in the RabbitHole database.")
            
            conn.commit()
            logging.info("Encrypted SQLite database created and initialized in your RabbitHole.")
        else:
            # Verify the database by executing a simple query
            cursor.execute("SELECT count(*) FROM api_keys;")
            logging.info("Encrypted SQLite database loaded successfully from your RabbitHole.")
        
        return conn
    except sqlite.DatabaseError as e:
        logging.error(f"Failed to initialize encrypted SQLite database in '{dbPath}': {e}")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------

def hashPassword(password):
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        bytes: The hashed password.
    """
    # Generate a bcrypt salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# Spacer for readability
# ------------------------------------------------------------------------------

def storePasswordHash(conn, hashedPassword):
    """
    Stores the hashed password in the 'users' table.

    Args:
        conn (sqlite.Connection): The SQLite connection object.
        hashedPassword (bytes): The hashed password to store.

    Returns:
        bool: True if the password was stored successfully, False otherwise.
    """
    try:
        logging.debug(f"Storing password hash: {hashedPassword}")
        cursor = conn.cursor()
        decodedHash = hashedPassword.decode('utf-8')  # Modified line
        cursor.execute("INSERT INTO users (password_hash) VALUES (?);", (decodedHash,))  # Modified line
        conn.commit()
        logging.info("User password hash stored successfully in the RabbitHole database.")
        return True
    except sqlite.IntegrityError:
        logging.warning("A password hash already exists in the RabbitHole database.")
        return False
    except UnicodeDecodeError as e:
        logging.error(f"Unicode decode error when storing password hash: {e}")
        return False
    except Exception as e:
        logging.error(f"Failed to store password hash in the RabbitHole database: {e}")
        return False

# Spacer for readability
# ------------------------------------------------------------------------------

def getStoredPasswordHash(conn):
    """
    Retrieves the stored hashed password from the 'users' table.

    Args:
        conn (sqlite.Connection): The SQLite connection object.

    Returns:
        bytes: The stored hashed password, or None if not found.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users LIMIT 1;")
        result = cursor.fetchone()
        if result:
            logging.info("Retrieved stored password hash from the RabbitHole database.")
            return result[0].encode('utf-8')
        else:
            logging.warning("No password hash found in the RabbitHole database.")
            return None
    except Exception as e:
        logging.error(f"Failed to retrieve password hash from the RabbitHole database: {e}")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------

def addApiKey(conn, label, iv, ciphertext):
    """
    Adds a new API key to the database.

    Args:
        conn (sqlite.Connection): The SQLite connection object.
        label (str): The label for the API key.
        iv (str): The base64-encoded initialization vector.
        ciphertext (str): The base64-encoded ciphertext of the API key.

    Returns:
        bool: True if the API key was added successfully, False otherwise.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO api_keys (label, iv, ciphertext) VALUES (?, ?, ?);",
            (label, iv, ciphertext)
        )
        conn.commit()
        logging.info(f"API key '{label}' added to the RabbitHole database.")
        return True
    except sqlite.IntegrityError:
        logging.warning(f"API key with label '{label}' already exists in the RabbitHole database.")
        return False
    except Exception as e:
        logging.error(f"Failed to add API key '{label}' to the RabbitHole database: {e}")
        return False

# Spacer for readability
# ------------------------------------------------------------------------------

def getAllApiKeys(conn):
    """
    Retrieves all API key labels from the database.

    Args:
        conn (sqlite.Connection): The SQLite connection object.

    Returns:
        list: A list of API key labels.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT label FROM api_keys;")
        labels = [row[0] for row in cursor.fetchall()]
        logging.info("Retrieved all API key labels from the RabbitHole database.")
        return labels
    except Exception as e:
        logging.error(f"Failed to retrieve API key labels from the RabbitHole database: {e}")
        return []

# Spacer for readability
# ------------------------------------------------------------------------------

def getApiKeyByLabel(conn, label):
    """
    Retrieves the IV and ciphertext for a specific API key label.

    Args:
        conn (sqlite.Connection): The SQLite connection object.
        label (str): The label of the API key to retrieve.

    Returns:
        tuple: A tuple containing the IV and ciphertext, or None if not found.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT iv, ciphertext FROM api_keys WHERE label = ?;", (label,))
        result = cursor.fetchone()
        if result:
            logging.info(f"Retrieved API key '{label}' from the RabbitHole database.")
            return result
        else:
            logging.warning(f"API key '{label}' not found in the RabbitHole database.")
            return None
    except Exception as e:
        logging.error(f"Failed to retrieve API key '{label}' from the RabbitHole database: {e}")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------
