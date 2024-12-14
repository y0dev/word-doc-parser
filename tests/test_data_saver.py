# This is a Python file.
import unittest
import os
import json
from utils.data_saver import DataSaver

class TestDataSaver(unittest.TestCase):
    def setUp(self):
        """ Sample data to be used in tests """
        self.test_data = {
            "headings": [{"text": "Sample Heading", "level": "Heading 1"}],
            "bold_phrases": ["Bold Text"],
            "italic_phrases": ["Italic Text"]
        }
        self.test_file = "tests/test_results.json"

    def tearDown(self):
        """ Remove test output files """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_to_json(self):
        saver = DataSaver(self.test_data, self.test_file)
        saver.save_to_json()

        # Check if the file was created
        self.assertTrue(os.path.exists(self.test_file))

        # Check the content of the file
        with open(self.test_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, self.test_data)

if __name__ == '__main__':
    unittest.main()
