# File: config/configManager.py

"""
RabbitHole/config/configManager.py

Manages configuration files and directories, ensuring defaults are in place.
Handles profile management, including adding and listing profiles.
"""

import os
import json
import logging
import platform

# Spacer for readability
# ------------------------------------------------------------------------------

def loadOrCreateConfig(osFlags):
    """
    Loads the configuration from 'config/config.json' or creates a default if it doesn't exist.
    Adjusts paths based on the detected OS.

    Args:
        osFlags (dict): Dictionary containing OS-related flags.

    Returns:
        dict: The loaded or default configuration.
    """
    configDir = getConfigDir(osFlags)

    if not os.path.exists(configDir):
        try:
            os.makedirs(configDir, exist_ok=True)
            logging.info(f"Created configuration directory at {configDir}.")
        except Exception as e:
            logging.error(f"Failed to create configuration directory: {e}")
            return None

    configFile = os.path.join(configDir, 'config.json')
    if not os.path.exists(configFile):
        defaultConfig = {
            "profiles": {},
            "logging": {
                "level": "INFO",
                "logDir": "log/"
            }
        }
        try:
            with open(configFile, 'w') as f:
                json.dump(defaultConfig, f, indent=4)
            logging.warning(f"Configuration file not found. Created default at {configFile}.")
            return defaultConfig
        except Exception as e:
            logging.error(f"Failed to create default configuration file: {e}")
            return None
    else:
        try:
            with open(configFile, 'r') as f:
                config = json.load(f)
            logging.info("Configuration file loaded successfully.")
            return config
        except json.JSONDecodeError as e:
            logging.error(f"Configuration file is invalid: {e}")
            # Attempt to recreate the default configuration
            defaultConfig = {
                "profiles": {},
                "logging": {
                    "level": "INFO",
                    "logDir": "log/"
                }
            }
            try:
                with open(configFile, 'w') as f:
                    json.dump(defaultConfig, f, indent=4)
                logging.warning(f"Invalid configuration file. Replaced with default at {configFile}.")
                return defaultConfig
            except Exception as e2:
                logging.error(f"Failed to recreate default configuration file: {e2}")
                return None

# Spacer for readability
# ------------------------------------------------------------------------------

def saveConfig(config, osFlags):
    """
    Saves the updated configuration back to the config file.

    Args:
        config (dict): The configuration dictionary to save.
        osFlags (dict): Dictionary containing OS-related flags.
    """
    configDir = getConfigDir(osFlags)
    configFile = os.path.join(configDir, 'config.json')
    try:
        with open(configFile, 'w') as f:
            json.dump(config, f, indent=4)
        logging.info("Configuration file updated successfully.")
    except Exception as e:
        logging.error(f"Failed to save configuration file: {e}")

# Spacer for readability
# ------------------------------------------------------------------------------

def addProfile(profileName, dbPath):
    """
    Adds a new profile to the configuration.

    Args:
        profileName (str): The name of the profile.
        dbPath (str): The path to the profile's database file.
    """
    config = loadOrCreateConfig(detectOS())
    if config is None:
        logging.error("Cannot add profile without a valid configuration.")
        return

    config['profiles'][profileName] = dbPath
    saveConfig(config, detectOS())
    logging.info(f"Profile '{profileName}' added with database '{dbPath}'.")

# Spacer for readability
# ------------------------------------------------------------------------------

def listProfiles():
    """
    Lists all existing profiles.

    Returns:
        list: A list of profile names.
    """
    config = loadOrCreateConfig(detectOS())
    if config and 'profiles' in config:
        return list(config['profiles'].keys())
    return []

# Spacer for readability
# ------------------------------------------------------------------------------

def getProfileDatabasePath(profileName):
    """
    Retrieves the database path for the given profile from the configuration.

    Args:
        profileName (str): The name of the profile.

    Returns:
        str: The database path associated with the profile, or None if not found.
    """
    config = loadOrCreateConfig(detectOS())
    if config and 'profiles' in config and profileName in config['profiles']:
        return config['profiles'][profileName]
    return None

# Spacer for readability
# ------------------------------------------------------------------------------

def getConfigDir(osFlags):
    """
    Determines the configuration directory based on the OS.

    Args:
        osFlags (dict): Dictionary containing OS-related flags.

    Returns:
        str: The path to the configuration directory.
    """
    if osFlags['IS_WINDOWS']:
        configDir = os.path.join(os.environ.get('APPDATA', 'C:\\'), 'RabbitHole', 'config')
    elif osFlags['IS_MAC'] or osFlags['IS_LINUX']:
        configDir = os.path.expanduser('~/RabbitHole/config')
    elif osFlags['IS_ANDROID']:
        configDir = os.path.expanduser('~/RabbitHole/config')  # Adjust as needed for Android
    else:
        configDir = 'config'  # Fallback
    return configDir

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
