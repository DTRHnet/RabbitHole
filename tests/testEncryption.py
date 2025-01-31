# File: tests/testEncryption.py

"""
RabbitHole/tests/testEncryption.py

Unit tests for the encryption module.
"""

import unittest
from encryption.encrypt import deriveKey, encryptApiKey
from encryption.decrypt import decryptApiKey
import os

# Spacer for readability
# ------------------------------------------------------------------------------

class TestEncryptionModule(unittest.TestCase):
    """
    Test cases for the encryption and decryption functions.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.password = "TestPassword123!"
        self.salt = os.urandom(16)
        self.key = deriveKey(self.password, self.salt)
        self.apiKey = "SensitiveAPIKey123456"

    def test_encryptDecryptApiKey(self):
        """
        Test that an API key can be encrypted and then decrypted back to its original value.
        """
        iv, ciphertext = encryptApiKey(self.apiKey, self.key)
        self.assertIsNotNone(iv)
        self.assertIsNotNone(ciphertext)

        decryptedKey = decryptApiKey(iv, ciphertext, self.key)
        self.assertEqual(self.apiKey, decryptedKey)

    def test_differentIvProducesDifferentCiphertext(self):
        """
        Test that encrypting the same API key with different IVs produces different ciphertexts.
        """
        iv1, ciphertext1 = encryptApiKey(self.apiKey, self.key)
        iv2, ciphertext2 = encryptApiKey(self.apiKey, self.key)
        self.assertNotEqual(ciphertext1, ciphertext2)

    def test_decryptWithWrongKeyFails(self):
        """
        Test that decryption fails when using an incorrect key.
        """
        iv, ciphertext = encryptApiKey(self.apiKey, self.key)
        wrongKey = deriveKey("WrongPassword", self.salt)
        decryptedKey = decryptApiKey(iv, ciphertext, wrongKey)
        self.assertIsNone(decryptedKey)

# Spacer for readability
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
