# File: tests/testStorage.py

"""
RabbitHole/tests/testStorage.py

Unit tests for the storage module.
"""

import unittest
from unittest.mock import MagicMock, patch
from storage.storage import loadApiKeys, retrieveApiKey, addApiKeySecurely
from storage.database import initializeDatabase, addApiKey, getAllApiKeys, getApiKeyByLabel
from encryption.encrypt import encryptApiKey
import os
import tempfile
import shutil

# Spacer for readability
# ------------------------------------------------------------------------------

class TestStorageModule(unittest.TestCase):
    """
    Test cases for the storage module.
    """

    def setUp(self):
        """
        Set up a temporary database for testing.
        """
        self.tempDir = tempfile.mkdtemp()
        self.dbPath = os.path.join(self.tempDir, 'test_api_keys.db')
        self.password = "TestPassword123!"
        from encryption.encrypt import deriveKey
        self.salt = os.urandom(16)
        self.key = deriveKey(self.password, self.salt)
        self.conn = initializeDatabase(self.dbPath, self.key)
        self.apiKey = "TestAPIKey"

    def tearDown(self):
        """
        Clean up the temporary directory after tests.
        """
        shutil.rmtree(self.tempDir)

    def test_addLoadApiKey(self):
        """
        Test adding an API key and loading it from the database.
        """
        label = "TestService"
        iv, ciphertext = encryptApiKey(self.apiKey, self.key)
        success = addApiKey(self.conn, label, iv, ciphertext)
        self.assertTrue(success)

        apiKeys = loadApiKeys(self.conn)
        self.assertEqual(len(apiKeys), 1)
        self.assertEqual(apiKeys[0]['label'], label)

    def test_retrieveApiKey(self):
        """
        Test retrieving and decrypting an API key.
        """
        label = "TestService"
        iv, ciphertext = encryptApiKey(self.apiKey, self.key)
        addApiKey(self.conn, label, iv, ciphertext)

        decryptedKey = retrieveApiKey(self.conn, label, self.key)
        self.assertEqual(decryptedKey, self.apiKey)

    def test_addDuplicateLabel(self):
        """
        Test that adding an API key with a duplicate label fails.
        """
        label = "TestService"
        iv, ciphertext = encryptApiKey(self.apiKey, self.key)
        success = addApiKey(self.conn, label, iv, ciphertext)
        self.assertTrue(success)

        # Attempt to add the same label again
        successDuplicate = addApiKey(self.conn, label, iv, ciphertext)
        self.assertFalse(successDuplicate)

# Spacer for readability
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
