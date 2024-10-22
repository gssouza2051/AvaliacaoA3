import unittest
from unittest.mock import patch
import main

class TestMain(unittest.TestCase):

    @patch('main.main')
    def test_main(self,mock_main):
        mock_main.return_value  = 'one'
        self.assertEqual(main(), 3)

if __name__ == "__main__":
    unittest.main()
