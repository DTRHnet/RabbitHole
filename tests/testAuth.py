# File: tests/testAuth.py

"""
RabbitHole/tests/testAuth.py

Unit tests for the authentication module.
"""

import unittest
from unittest.mock import patch, MagicMock
from auth.password import hashPassword, verifyPassword, authenticateUser
from storage.database import getStoredPasswordHash

# Spacer for readability
# ------------------------------------------------------------------------------

class TestAuthModule(unittest.TestCase):
    """
    Test cases for the authentication module.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        # Mock stored password hash
        self.password = "SecureP@ssw0rd!"
        self.hashed = hashPassword(self.password)

    @patch('storage.database.getStoredPasswordHash')
    def test_verifyPasswordSuccess(self, mock_get_hash):
        """
        Test that verifyPassword returns True for correct password.
        """
        mock_get_hash.return_value = self.hashed
        self.assertTrue(verifyPassword(self.hashed, self.password))

    @patch('storage.database.getStoredPasswordHash')
    def test_verifyPasswordFailure(self, mock_get_hash):
        """
        Test that verifyPassword returns False for incorrect password.
        """
        mock_get_hash.return_value = self.hashed
        self.assertFalse(verifyPassword(self.hashed, "WrongPassword"))

    @patch('builtins.input', return_value='SecureP@ssw0rd!')
    @patch('storage.database.getStoredPasswordHash')
    def test_authenticateUserSuccess(self, mock_get_hash, mock_input):
        """
        Test successful user authentication.
        """
        mock_get_hash.return_value = self.hashed
        with patch('getpass.getpass', return_value=self.password):
            self.assertTrue(authenticateUser())

    @patch('builtins.input', return_value='WrongPassword')
    @patch('storage.database.getStoredPasswordHash')
    def test_authenticateUserFailure(self, mock_get_hash, mock_input):
        """
        Test failed user authentication.
        """
        mock_get_hash.return_value = self.hashed
        with patch('getpass.getpass', return_value='WrongPassword'):
            self.assertFalse(authenticateUser())

# Spacer for readability
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
