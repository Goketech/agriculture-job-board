import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from matching_engine import calculate_match_score, match_jobs_to_worker, match_workers_to_job

class TestMatching(unittest.TestCase):
    def test_calculate_match_score_function_exists(self):
        self.assertTrue(callable(calculate_match_score))

    def test_match_jobs_to_worker_function_exists(self):
        self.assertTrue(callable(match_jobs_to_worker))

    def test_match_workers_to_job_function_exists(self):
        self.assertTrue(callable(match_workers_to_job))

if __name__ == "__main__":
    unittest.main()