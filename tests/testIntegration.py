# File: tests/testIntegration.py

"""
RabbitHole/tests/testIntegration.py

Integration tests for the entire API Key Manager workflow.
"""

import unittest
from unittest.mock import patch
from storage.storage import addApiKeySecurely, loadApiKeys, retrieveApiKey
from storage.database import initializeDatabase
from encryption.encrypt import deriveKey, encryptApiKey
import os
import tempfile
import shutil

# Spacer for readability
# ------------------------------------------------------------------------------

class TestIntegration(unittest.TestCase):
    """
    Integration test cases for the RabbitHole.
    """

    def setUp(self):
        """
        Set up a temporary database and encryption key for testing.
        """
        self.tempDir = tempfile.mkdtemp()
        self.dbPath = os.path.join(self.tempDir, 'test_api_keys.db')
        self.password = "IntegrationTestPass!"
        from encryption.encrypt import deriveKey
        self.salt = os.urandom(16)
        self.key = deriveKey(self.password, self.salt)
        # Create the magic string in the first line
        with open(self.dbPath, 'w') as f:
            f.write("RABBITHOLE_DB_V1\n")
        self.conn = initializeDatabase(self.dbPath, self.key)

    def tearDown(self):
        """
        Clean up the temporary directory after tests.
        """
        shutil.rmtree(self.tempDir)

    @patch('builtins.input', side_effect=['IntegrationService'])
    @patch('getpass.getpass', return_value='IntegrationAPIKey123!')
    def test_fullWorkflowAddRetrieve(self, mock_getpass, mock_input):
        """
        Test the full workflow of adding an API key and retrieving it.
        """
        # Add the API key
        success = addApiKeySecurely(self.conn, self.key)
        self.assertTrue(success)

        # Load the API keys
        apiKeys = loadApiKeys(self.conn)
        self.assertEqual(len(apiKeys), 1)
        self.assertEqual(apiKeys[0]['label'], 'IntegrationService')

        # Retrieve the API key
        decryptedKey = retrieveApiKey(self.conn, 'IntegrationService', self.key)
        self.assertEqual(decryptedKey, 'IntegrationAPIKey123!')

    @patch('builtins.input', side_effect=[''])
    @patch('getpass.getpass', return_value='')
    def test_addApiKeyEmptyFields(self, mock_getpass, mock_input):
        """
        Test adding an API key with empty label and API key.
        """
        # Attempt to add the API key
        with patch('builtins.print') as mockPrint:
            success = addApiKeySecurely(self.conn, self.key)
            self.assertFalse(success)
            mockPrint.assert_any_call("🚫 Label cannot be empty.")

# Spacer for readability
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
