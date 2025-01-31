# File: ui/clipboard.py

"""
RabbitHole/ui/clipboard.py

Manages secure copying of API keys to the clipboard with automatic clearing.
"""

import pyperclip
import threading
import logging
import atexit

# Spacer for readability
# ------------------------------------------------------------------------------

timer = None  # Global timer for clipboard clearing

def copyToClipboard(text, timeout=30):
    """
    Copies the given text to the clipboard and schedules it to be cleared after a timeout.

    Args:
        text (str): The text to copy to the clipboard.
        timeout (int, optional): Time in seconds before the clipboard is cleared. Defaults to 30.
    """
    global timer
    try:
        pyperclip.copy(text)
        logging.info("API key copied to clipboard.")

        # Cancel any existing timer
        if timer:
            timer.cancel()

        # Define a function to clear the clipboard
        def clearClipboard():
            pyperclip.copy('')
            logging.info("Clipboard cleared after timeout.")

        # Start a new timer to clear the clipboard
        timer = threading.Timer(timeout, clearClipboard)
        timer.start()
    except Exception as e:
        logging.error(f"Failed to copy to clipboard: {e}")

# Spacer for readability
# ------------------------------------------------------------------------------

def clearClipboardOnExit():
    """
    Clears the clipboard when the application exits.
    """
    try:
        pyperclip.copy('')
        logging.info("Clipboard cleared on exit.")
    except Exception as e:
        logging.error(f"Failed to clear clipboard on exit: {e}")

# Register the clear function to be called on exit
atexit.register(clearClipboardOnExit)

# Spacer for readability
# ------------------------------------------------------------------------------
