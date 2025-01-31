# File: loggingSetup.py

"""
RabbitHole/loggingSetup.py

Sets up the logging configuration for RabbitHole.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import sys

def setupLogging():
    """
    Configures the logging settings, including log file rotation.
    """
    # Define log directory and file
    logDir = 'log'
    logFile = os.path.join(logDir, 'rabbithole.log')

    # Create log directory if it doesn't exist
    os.makedirs(logDir, exist_ok=True)

    # Create a rotating file handler
    handler = RotatingFileHandler(logFile, maxBytes=1048576, backupCount=5)  # 1MB per file, 5 backups
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Get the root logger and set level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
