# File: tests/testUI.py

"""
RabbitHole/tests/testUI.py

Unit tests for the UI module.
"""

import unittest
from unittest.mock import patch, MagicMock
from ui.fzfInterface import selectItem, listDatabaseFiles
from ui.clipboard import copyToClipboard
import pyperclip
import os

# Spacer for readability
# ------------------------------------------------------------------------------

class TestUIModule(unittest.TestCase):
    """
    Test cases for the UI module.
    """

    @patch('subprocess.Popen')
    def test_selectItemSuccess(self, mock_popen):
        """
        Test that selectItem returns the selected label correctly.
        """
        mockProcess = MagicMock()
        mockProcess.communicate.return_value = ('SelectedLabel\n', None)
        mock_popen.return_value = mockProcess

        labels = ['ServiceA', 'ServiceB', 'ServiceC']
        selected = selectItem(labels)
        self.assertEqual(selected, 'SelectedLabel')

    @patch('subprocess.Popen')
    def test_selectItemNoSelection(self, mock_popen):
        """
        Test that selectItem returns None when no selection is made.
        """
        mockProcess = MagicMock()
        mockProcess.communicate.return_value = ('\n', None)
        mock_popen.return_value = mockProcess

        labels = ['ServiceA', 'ServiceB', 'ServiceC']
        selected = selectItem(labels)
        self.assertIsNone(selected)

    @patch('pyperclip.copy')
    def test_copyToClipboard(self, mock_copy):
        """
        Test that copyToClipboard copies the text and clears it after timeout.
        """
        with patch('threading.Timer') as mockTimer:
            copyToClipboard("SensitiveAPIKey", timeout=5)
            mock_copy.assert_called_with("SensitiveAPIKey")
            mockTimer.assert_called_with(5, unittest.mock.ANY)
            mockTimer.return_value.start.assert_called_once()

    def test_listDatabaseFiles(self):
        """
        Test that listDatabaseFiles returns only valid database files.
        """
        with patch('os.listdir') as mockListdir:
            # Mock files with and without the magic string
            mockListdir.return_value = ['valid_db.db', 'invalid_db.db', 'notes.txt']
            with patch('builtins.open', mock_open(read_data="RABBITHOLE_DB_V1\n")):
                dbFiles = listDatabaseFiles('data/')
                self.assertIn('valid_db.db', dbFiles)
                self.assertNotIn('invalid_db.db', dbFiles)
                self.assertNotIn('notes.txt', dbFiles)

# Spacer for readability
# ------------------------------------------------------------------------------

from unittest.mock import mock_open

if __name__ == '__main__':
    unittest.main()
