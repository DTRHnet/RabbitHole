# File: main.py

"""
RabbitHole/main.py

Main entry point for the RabbitHole application.
Handles profile selection or creation and manages API keys securely.
"""

import sys
import os
import logging
import platform
from auth.password import authenticateUser
from storage.storage import loadApiKeys, retrieveApiKey, addApiKeySecurely
from encryption.encrypt import getEncryptionKey
from ui.fzfInterface import selectItem, listDatabaseFiles
from ui.clipboard import copyToClipboard
from config.configManager import loadOrCreateConfig, addProfile, listProfiles, getProfileDatabasePath
import binascii  # Added import for binascii

# Spacer for readability
# ------------------------------------------------------------------------------

def setupLoggingModule():
    """
    Initializes the logging module with rolling file handlers.
    Ensures logs are stored securely without exposing sensitive information.
    """
    import loggingSetup  # Assume a separate module for logging setup
    
    loggingSetup.setupLogging()
    logging.info("Logging setup complete.")

# Spacer for readability
# ------------------------------------------------------------------------------

def getUserPassword():
    """
    Prompts the user to enter their password securely.

    Returns:
        str: The password entered by the user.
    """
    import getpass
    password = getpass.getpass("🔒 Enter your secret password: ")
    return password

# Spacer for readability
# ------------------------------------------------------------------------------

def verifyDbMagicString(dbPath):
    """
    Verifies that the database file contains the expected magic string in the first line.

    Args:
        dbPath (str): Path to the database file.

    Returns:
        bool: True if the magic string is present, False otherwise.
    """
    MAGIC_STRING = "RABBITHOLE_DB_V1"
    try:
        with open(dbPath, 'r') as dbFile:
            firstLine = dbFile.readline().strip()
            if firstLine == MAGIC_STRING:
                logging.info(f"Database '{dbPath}' verified successfully.")
                return True
            else:
                logging.warning(f"Database '{dbPath}' failed magic string verification.")
                return False
    except Exception as e:
        logging.error(f"Failed to verify magic string for database '{dbPath}': {e}")
        return False

# Spacer for readability
# ------------------------------------------------------------------------------

def createNewDatabase(osFlags):
    """
    Guides the user through creating a new database file.
    Prompts for location and name, and initializes the database.

    Args:
        osFlags (dict): Dictionary containing OS-related flags.

    Returns:
        tuple: A tuple containing the profile name and the SQLite connection object, or (None, None) if creation fails.
    """
    from encryption.encrypt import deriveKey
    import getpass

    try:
        print("🐰 Creating a new profile in your RabbitHole.")
        profileName = input("✨ Enter a unique profile name: ").strip()
        if not profileName:
            print("🚫 Profile name cannot be empty.")
            logging.warning("Attempted to create a profile with an empty name.")
            return None, None

        # Check if profile already exists
        if profileName in listProfiles():
            print(f"🚫 Profile '{profileName}' already exists.")
            logging.info(f"Profile '{profileName}' already exists.")
            # Proceed to connect to the existing profile
            dbPath = getProfileDatabasePath(profileName)
            if not dbPath:
                print(f"🚫 Database path for profile '{profileName}' not found.")
                logging.error(f"Database path for profile '{profileName}' not found in config.")
                return None, None

            if not os.path.isfile(dbPath):
                print(f"🚫 Database file '{dbPath}' does not exist.")
                logging.error(f"Database file '{dbPath}' for profile '{profileName}' does not exist.")
                return None, None

            # Prompt for password to derive encryption key
            password = getUserPassword()
            encryptionKey = getEncryptionKey(password)
            if encryptionKey is None:
                print("🚫 Failed to derive encryption key. Exiting.")
                logging.critical("Encryption key derivation failed during profile connection.")
                return None, None

            # Initialize database connection
            from storage.database import initializeDatabase
            conn = initializeDatabase(dbPath, encryptionKey)
            if conn:
                logging.info(f"Profile '{profileName}' loaded successfully with database '{dbPath}'.")
                return profileName, conn
            else:
                print("🚫 Failed to initialize the database.")
                logging.error(f"Failed to initialize the database '{dbPath}' for profile '{profileName}'.")
                return None, None

        print("📁 Specify the location for the new database file.")
        dirPrompt = "🔍 Enter the directory where you want to create the database: "
        if osFlags['IS_WINDOWS']:
            dirPrompt = "🔍 Enter the directory path (e.g., C:\\Users\\Username\\Documents): "
        elif osFlags['IS_MAC']:
            dirPrompt = "🔍 Enter the directory path (e.g., /Users/Username/Documents): "
        elif osFlags['IS_LINUX']:
            dirPrompt = "🔍 Enter the directory path (e.g., /home/username/Documents): "
        elif osFlags['IS_ANDROID']:
            dirPrompt = "🔍 Enter the directory path (e.g., /data/data/com.termux/files/home/Documents): "

        dirPath = input(dirPrompt).strip()
        if not os.path.isdir(dirPath):
            print("🚫 Invalid directory path.")
            logging.warning(f"Invalid directory path entered: {dirPath}")
            return None, None

        dbName = input("📄 Enter the name for the new database file (e.g., my_api_keys.db): ").strip()
        if not dbName.endswith('.db'):
            dbName += '.db'

        dbPath = os.path.join(dirPath, dbName)

        if os.path.exists(dbPath):
            print(f"🚫 File '{dbPath}' already exists.")
            logging.warning(f"Attempted to create a database that already exists: {dbPath}")
            # Proceed to connect to the existing database
            password = getUserPassword()
            encryptionKey = getEncryptionKey(password)
            if encryptionKey is None:
                print("🚫 Failed to derive encryption key. Exiting.")
                logging.critical("Encryption key derivation failed during profile connection.")
                return None, None

            from storage.database import initializeDatabase
            conn = initializeDatabase(dbPath, encryptionKey)
            if conn:
                logging.info(f"Existing database '{dbPath}' connected successfully.")
                return profileName, conn
            else:
                print("🚫 Failed to initialize the existing database.")
                logging.error(f"Failed to initialize the existing database '{dbPath}'.")
                return None, None

        # Initialize the encrypted database without writing a magic string
        password = getUserPassword()
        encryptionKey = getEncryptionKey(password)
        if encryptionKey is None:
            print("🚫 Failed to derive encryption key. Database not initialized.")
            logging.critical("Encryption key derivation failed during database creation.")
            return None, None

        from storage.database import initializeDatabase, storePasswordHash, hashPassword
        conn = initializeDatabase(dbPath, encryptionKey)
        if conn:
            # Hash and store the user's password
            hashedPassword = hashPassword(password)
            if storePasswordHash(conn, hashedPassword):
                logging.info(f"Password hash stored successfully for profile '{profileName}'.")
            else:
                print("🚫 Failed to store password hash. Aborting profile creation.")
                logging.error(f"Failed to store password hash for profile '{profileName}'.")
                return None, None

            # Add profile to config
            addProfile(profileName, dbPath)
            return profileName, conn
        else:
            print("🚫 Failed to initialize the database.")
            logging.error(f"Failed to initialize the database '{dbPath}'.")
            return None, None

    except Exception as e:
        print(f"🚫 An error occurred while creating the database: {e}")
        logging.error(f"Exception during database creation: {e}")
        return None, None

    # Spacer for readability
    # ------------------------------------------------------------------------------

def selectExistingProfile(osFlags):
    """
    Allows the user to select an existing profile using an fzf-style interface.

    Args:
        osFlags (dict): Dictionary containing OS-related flags.

    Returns:
        tuple: A tuple containing the selected profile name and the SQLite connection object, or (None, None) if selection fails.
    """
    try:
        profiles = listProfiles()
        if not profiles:
            print("🐰 No profiles found. You need to create a new profile first.")
            logging.info("No profiles available for selection.")
            return None, None

        selectedProfile = selectItem(profiles)
        if selectedProfile:
            dbPath = getProfileDatabasePath(selectedProfile)
            if not dbPath:
                print(f"🚫 Database path for profile '{selectedProfile}' not found.")
                logging.error(f"Database path for profile '{selectedProfile}' not found in config.")
                return None, None

            if not os.path.isfile(dbPath):
                print(f"🚫 Database file '{dbPath}' does not exist.")
                logging.error(f"Database file '{dbPath}' for profile '{selectedProfile}' does not exist.")
                return None, None

            # Prompt for password to derive encryption key
            password = getUserPassword()
            encryptionKey = getEncryptionKey(password)
            if encryptionKey is None:
                print("🚫 Failed to derive encryption key. Exiting.")
                logging.critical("Encryption key derivation failed during profile selection.")
                return None, None

            # Initialize database connection
            from storage.database import initializeDatabase
            conn = initializeDatabase(dbPath, encryptionKey)
            if conn:
                logging.info(f"Profile '{selectedProfile}' loaded successfully with database '{dbPath}'.")
                return selectedProfile, conn
            else:
                print("🚫 Failed to initialize the database.")
                logging.error(f"Failed to initialize the database '{dbPath}' for profile '{selectedProfile}'.")
                return None, None
        else:
            print("🐰 No profile selected.")
            logging.info("No profile was selected by the user.")
            return None, None
    except Exception as e:
        print(f"🚫 An error occurred while selecting the profile: {e}")
        logging.error(f"Exception during profile selection: {e}")
        return None, None

# Spacer for readability
# ------------------------------------------------------------------------------

def main():
    """
    Orchestrates the workflow of RabbitHole, handling profile selection or creation,
    user authentication, API key management, and secure clipboard operations.
    """
    # Step 1: Detect OS and set flags
    osFlags = detectOS()

    # Step 2: Setup Logging
    setupLoggingModule()

    # Step 3: Load Configuration
    config = loadOrCreateConfig(osFlags)
    if config is None:
        print("🚫 Failed to load configuration. Exiting.")
        logging.critical("Configuration loading failed. Exiting application.")
        sys.exit(1)

    # Spacer for readability
    # ------------------------------------------------------------------------------

    # Step 4: Handle Profile Selection or Creation
    print("🐰 Welcome to RabbitHole!")
    profiles = listProfiles()
    if not profiles:
        print("🐰 No profiles detected. Please create a new profile.")
        profileName, conn = createNewDatabase(osFlags)
        if not profileName:
            print("🚫 Failed to create a new profile. Exiting.")
            logging.critical("Profile creation failed. Exiting application.")
            sys.exit(1)
    else:
        choice = input("🐰 Would you like to select an existing profile? (y/n): ").strip().lower()
        if choice == 'y':
            profileName, conn = selectExistingProfile(osFlags)
            if not profileName:
                print("🚫 Failed to select a valid profile. Exiting.")
                logging.critical("Profile selection failed. Exiting application.")
                sys.exit(1)
        else:
            profileName, conn = createNewDatabase(osFlags)
            if not profileName:
                print("🚫 Failed to create a new profile. Exiting.")
                logging.critical("Profile creation failed. Exiting application.")
                sys.exit(1)

    # Spacer for readability
    # ------------------------------------------------------------------------------

    # Step 5: Authenticate User
    if not authenticateUser(conn):
        print("🚫 Authentication failed.")
        logging.warning("User failed to authenticate.")
        sys.exit(1)

    # Spacer for readability
    # ------------------------------------------------------------------------------

    # Step 6: Load API Keys
    encryptionKey = getEncryptionKey(getUserPassword())
    if encryptionKey is None:
        print("🚫 Failed to derive encryption key. Exiting.")
        logging.critical("Encryption key derivation failed. Exiting application.")
        sys.exit(1)

    apiKeys = loadApiKeys(conn)
    if not apiKeys:
        print("🐰 No API keys found. Would you like to add one? (y/n): ", end='')
        choice = input().strip().lower()
        if choice == 'y':
            addApiKeySecurely(conn, encryptionKey)
            apiKeys = loadApiKeys(conn)
            if not apiKeys:
                print("🐰 No API keys added. Exiting.")
                logging.info("No API keys were added by the user.")
                sys.exit(0)
        else:
            print("🐰 No API keys to manage. Exiting.")
            logging.info("User chose not to add any API keys.")
            sys.exit(0)

    # Spacer for readability
    # ------------------------------------------------------------------------------

    # Step 7: Select API Key via fzf
    selectedLabel = selectItem([key['label'] for key in apiKeys])
    if not selectedLabel:
        print("🐰 No API key selected.")
        logging.info("No API key was selected by the user.")
        sys.exit(0)

    # Spacer for readability
    # ------------------------------------------------------------------------------

    # Step 8: Retrieve and Decrypt Selected API Key
    decryptedKey = retrieveApiKey(conn, selectedLabel, encryptionKey)
    if decryptedKey is None:
        print(f"🚫 Failed to retrieve API key for '{selectedLabel}'.")
        logging.error(f"Failed to retrieve API key for '{selectedLabel}'.")
        sys.exit(1)

    # Spacer for readability
    # ------------------------------------------------------------------------------

    # Step 9: Copy to Clipboard
    copyToClipboard(decryptedKey)
    print(f"🔑 API key for '{selectedLabel}' pulled from the RabbitHole and copied to clipboard.")
    logging.info(f"API key for '{selectedLabel}' pulled from the RabbitHole and copied to clipboard.")

# Spacer for readability
# ------------------------------------------------------------------------------

def detectOS():
    """
    Detects the host operating system and architecture.
    Sets flags accordingly for cross-platform operations.

    Returns:
        dict: A dictionary containing OS-related flags.
    """
    osName = platform.system()
    architecture = platform.machine()
    logging.info(f"Detected OS: {osName}, Architecture: {architecture}")

    osFlags = {
        'IS_WINDOWS': False,
        'IS_MAC': False,
        'IS_LINUX': False,
        'IS_ANDROID': False,
        'ARCHITECTURE': architecture
    }

    if osName == 'Windows':
        osFlags['IS_WINDOWS'] = True
    elif osName == 'Darwin':
        osFlags['IS_MAC'] = True
    elif osName == 'Linux':
        # Additional check for Android
        if 'ANDROID_ROOT' in os.environ:
            osFlags['IS_ANDROID'] = True
        else:
            osFlags['IS_LINUX'] = True
    else:
        logging.warning(f"Unsupported OS: {osName}")

    return osFlags

# Spacer for readability
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
