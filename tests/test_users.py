import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from user_management import register_farmer, register_worker, update_worker_skills
from database import execute_query, fetch_one

class TestUsers(unittest.TestCase):
    def test_register_farmer_function_exists(self):
        self.assertTrue(callable(register_farmer))

    def test_register_worker_function_exists(self):
        self.assertTrue(callable(register_worker))

    def test_update_worker_skills_function_exists(self):
        self.assertTrue(callable(update_worker_skills))

if __name__ == "__main__":
    unittest.main()
