# File: ui/fzfInterface.py

"""
RabbitHole/ui/fzfInterface.py

Implements the fzf-style fuzzy finder interface for selecting API keys and profiles.
"""

import subprocess
import logging
import os

# Spacer for readability
# ------------------------------------------------------------------------------

def selectItem(labels):
    """
    Presents a fuzzy finder interface to the user for selecting an API key label or profile.

    Args:
        labels (list): A list of API key labels or profile names to display.

    Returns:
        str: The selected label or profile name, or None if no selection was made.
    """
    try:
        # Join the labels into a single string separated by newlines
        inputLabels = '\n'.join(labels)

        # Initialize the subprocess for fzf
        fzf = subprocess.Popen(['fzf'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        # Communicate the labels to fzf and capture the selected label
        selectedLabel, _ = fzf.communicate(inputLabels)
        selectedLabel = selectedLabel.strip()

        if selectedLabel:
            logging.info(f"User selected: {selectedLabel}")
            return selectedLabel
        else:
            logging.info("No selection was made by the user.")
            return None
    except Exception as e:
        logging.error(f"Failed to invoke fzf: {e}")
        return None

# Spacer for readability
# ------------------------------------------------------------------------------

def listDatabaseFiles(directory):
    """
    Lists all database files in the specified directory that contain the magic string.

    Args:
        directory (str): The directory to search for database files.

    Returns:
        list: A list of valid database file names.
    """
    MAGIC_STRING = "RABBITHOLE_DB_V1"
    dbFiles = []
    try:
        for file in os.listdir(directory):
            if file.endswith('.db'):
                dbPath = os.path.join(directory, file)
                with open(dbPath, 'r') as dbFile:
                    firstLine = dbFile.readline().strip()
                    if firstLine == MAGIC_STRING:
                        dbFiles.append(file)
        logging.info(f"Found {len(dbFiles)} valid database files in '{directory}'.")
        return dbFiles
    except FileNotFoundError:
        logging.warning(f"Directory '{directory}' does not exist.")
        return []
    except Exception as e:
        logging.error(f"Error while listing database files: {e}")
        return []

# Spacer for readability
# ------------------------------------------------------------------------------
