import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from job_management import post_job, view_all_jobs, update_job_status
from database import execute_query, fetch_one

class TestJobs(unittest.TestCase):
    def test_post_job_function_exists(self):
        self.assertTrue(callable(post_job))

    def test_view_all_jobs_function_exists(self):
        self.assertTrue(callable(view_all_jobs))

    def test_update_job_status_function_exists(self):
        self.assertTrue(callable(update_job_status))

if __name__ == "__main__":
    unittest.main()